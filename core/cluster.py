import os
import artm
import re
import glob
import pymystem3

import numpy as np
import pandas as pd

from colour import Color
from PIL import Image, ImageDraw
from wordcloud import WordCloud
from operator import itemgetter
from collections import Counter, defaultdict
from gensim import corpora, models
from gensim.summarization import summarize, keywords
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation


class DatasetCleaner(object):
    def __init__(self, csv_path):
        self.csv_path = csv_path
        self.texts = pd.read_csv(csv_path)['text'].tolist()

    def clean_texts_from_junk(self):
        plain_publications = [text.strip().lower() for text in self.texts]
        for i, publication in enumerate(plain_publications):
            plain_publications[i] = ' '.join(list(filter(None, re.split('[^а-я]', publication))))

        return plain_publications

    def get_sentiments_for_texts(self):
        return pd.read_csv(self.csv_path)['color'].tolist()


class DictionaryCreator(object):
    def __init__(self):
        self.stop_words = set(stopwords.words('russian'))
        ext = ['еще', 'него', 'сказать', 'а', 'ж', 'нее', 'со', 'же', 'ней', 'более', 'жизнь', 'нельзя', 'так', 'за',
               'такой',
               'зачем', 'ни', 'там', 'будто', 'здесь', 'нибудь', 'тебя', 'бы', 'и', 'никогда', 'тем', 'был', 'из',
               'ним', 'теперь',
               'была', 'из-за', 'них', 'то', 'были', 'или', 'но', 'ну', 'в', 'на', 'как', 'ксения', 'бла', 'это',
               'очень']

        self.stop_words.update(ext)

    def create_dictionary_from_texts(self, texts):
        texts = self._remove_stop_words(texts)
        texts = self._remove_words_that_appear_only_once(texts)
        texts = self._lemmatize_words(texts)

        return self._create_and_save_dictionary(texts)

    def get_texts_clean(self, texts):
        texts = self._remove_stop_words(texts)
        texts = self._remove_words_that_appear_only_once(texts)
        texts = self._lemmatize_words(texts)

        return texts

    def _remove_stop_words(self, texts):
        return [[word for word in text.lower().split() if word not in self.stop_words] for text in texts]

    def _create_and_save_dictionary(self, texts):
        dictionary = corpora.Dictionary(texts)
        dictionary.save('comments.dict')

        return dictionary

    def _remove_words_that_appear_only_once(self, texts):
        frequency = defaultdict(int)
        for text in texts:
            for token in text:
                frequency[token] += 1

        return [[token for token in text if frequency[token] > 1] for text in texts]

    def _lemmatize_words(self, texts):
        mystem = pymystem3.Mystem()
        return [[mystem.lemmatize(token)[0] for token in text] for text in texts]


class CorpusCreator(object):
    PATH = os.path.dirname(__file__)
    COMMENTS_DICT_FILE_NAME = os.path.join(PATH, '../forum_analyzer/preprocessor/resources', "comments.dict")
    COMMENTS_MM_FILE_NAME = os.path.join(PATH, '../forum_analyzer/preprocessor/resources', "comments.mm")

    def __init__(self, texts, sentiments, dictionary=None):
        if (os.path.exists(self.COMMENTS_DICT_FILE_NAME) and os.path.exists(self.COMMENTS_MM_FILE_NAME)):
            self.dictionary = corpora.Dictionary.load(self.COMMENTS_DICT_FILE_NAME)
            self.corpus = corpora.MmCorpus(self.COMMENTS_MM_FILE_NAME)
        else:
            self.dictionary = dictionary
            self.corpus = [self.dictionary.doc2bow([token for token in text]) for text in texts]

            corpora.MmCorpus.serialize(self.COMMENTS_MM_FILE_NAME, self.corpus)

        self.texts = np.asarray(texts)
        self.stop_words = DictionaryCreator().stop_words
        self.sentiments = sentiments


class ClusterTopicsHelper(object):
    PATH = os.path.dirname(__file__)
    RESOURCES_FOLDER = os.path.join(PATH, '../forum_analyzer/preprocessor/resources')

    CLUSTERS_FILENAME = os.path.join(PATH, '../forum_analyzer/preprocessor/resources', 'clusters.csv')
    TAGS_FILENAME = os.path.join(PATH, '../forum_analyzer/preprocessor/resources', 'tags.csv')
    COMMENTS_FILENAME = os.path.join(PATH, '../forum_analyzer/preprocessor/resources', 'comments.csv')
    TAGS_AND_COMMENTS = os.path.join(PATH, '../forum_analyzer/preprocessor/resources', 'tags_comments.csv')

    MODELS_FILENAME = os.path.join(PATH, '../forum_analyzer/preprocessor/resources', 'comm')

    CLUSTER_IMAGES_FILENAME = os.path.join(PATH, os.path.join('../forum_analyzer/preprocessor/resources', 'images'), '{}.png')

    ERROR_NOT_ENOUGH_POSTS_FOR_SUMMARY = 'Summary is not available for this cluster.'
    ERROR_NOT_ENOUGH_POSTS_FOR_TAGS = 'Keywords are not available for this cluster.'

    def __init__(self, corpus, num_of_clusters=5, num_of_texts_for_keywords=500, num_of_keywords_to_extract=500):
        self.corpus = corpus
        self.num_of_clusters = num_of_clusters
        self.num_of_texts_for_keywords = num_of_texts_for_keywords
        self.num_of_keywords_to_extract = num_of_keywords_to_extract

    def cluster_texts(self, clustering_method='artm', vectorizing_method='artm'):
        self._make_uci_dataset_from_corpus()

        corpus_vector_spaced = self._get_corpus_vector_representation(vectorizing_method)

        corpus_modeled = self._get_corpus_model(corpus_vector_spaced, clustering_method)

        comments_clusters = self._get_comments_clusters(corpus_modeled)
        self._save_comments(comments_clusters)

        cluster_summaries = self._get_cluster_summaries(comments_clusters)
        self._save_cluster(cluster_summaries)

        tags = self._get_keywords_for_corpus()
        self._save_tags(tags)

        tag_comment = self._get_tags_for_comments(tags)
        self._save_tag_comment(tag_comment)

    def _get_corpus_vector_representation(self, vectorizing_method='artm'):
        if 'gensim' == vectorizing_method:
            return self._get_tfidf_for_corpus()
        elif 'sklearn' == vectorizing_method:
            return self._get_frequencies_for_corpus()
        elif 'artm' == vectorizing_method:
            batch_vectorizer = None
            # if len(glob.glob(os.path.join(self.MODELS_FILENAME, '*.batch'))) < 1:
            batch_vectorizer = artm.BatchVectorizer(data_path=self.RESOURCES_FOLDER, data_format='bow_uci',
                                                    collection_name='comm', target_folder=self.MODELS_FILENAME)
            # else:
            #    batch_vectorizer = artm.BatchVectorizer(data_path=self.MODELS_FILENAME, data_format='batches')

            return {'batch_vectorizer': batch_vectorizer, 'dictionary': batch_vectorizer.dictionary}

    def _get_corpus_model(self, corpus_vector_spaced, clustering_method='artm'):
        if 'gensim' == clustering_method:
            return self._get_model_LSI(corpus_vector_spaced)
        elif 'sklearn' == clustering_method:
            return self._get_model_LDA(corpus_vector_spaced)
        elif 'artm' == clustering_method:
            batch_vectorizer = corpus_vector_spaced['batch_vectorizer']
            dictionary = corpus_vector_spaced['dictionary']

            topic_names = ['topic_{}'.format(i) for i in range(self.num_of_clusters)]

            model_artm = artm.ARTM(topic_names=topic_names, cache_theta=True,
                                   scores=[artm.PerplexityScore(name='PerplexityScore', dictionary=dictionary)],
                                   regularizers=[artm.SmoothSparseThetaRegularizer(name='SparseTheta', tau=-0.15)])

            model_artm.scores.add(artm.SparsityPhiScore(name='SparsityPhiScore'))
            model_artm.scores.add(artm.SparsityThetaScore(name='SparsityThetaScore'))
            model_artm.scores.add(artm.TopicKernelScore(name='TopicKernelScore', probability_mass_threshold=0.3))
            model_artm.scores.add(artm.TopTokensScore(name='TopTokensScore', num_tokens=10), overwrite=True)

            model_artm.regularizers.add(artm.SmoothSparsePhiRegularizer(name='SparsePhi', tau=-0.1))
            model_artm.regularizers['SparseTheta'].tau = -0.2
            model_artm.regularizers.add(artm.DecorrelatorPhiRegularizer(name='DecorrelatorPhi', tau=1.5e+5))

            model_artm.num_document_passes = 1

            model_artm.initialize(dictionary)
            model_artm.fit_offline(batch_vectorizer=batch_vectorizer, num_collection_passes=30)

            return model_artm.transform(batch_vectorizer=batch_vectorizer).T

    def _save_comments(self, comments_clusters):
        print(comments_clusters)

        cluster_sentiment = dict()
        for cc in comments_clusters:
            if cc[1] not in cluster_sentiment.keys():
                cluster_sentiment[cc[1]] = 0

            cluster_sentiment[cc[1]] += self.corpus.sentiments[cc[0] % len(self.corpus.sentiments)]

        cluster_sentiments = []
        for i in range(self.num_of_clusters):
            cluster_sentiments.append(cluster_sentiment[i])

        max_element = max(cluster_sentiments)

        for i in range(len(cluster_sentiments)):
            cluster_sentiments[i] = int((cluster_sentiments[i] / max_element) * 10)

        print(cluster_sentiments)

        red = Color("red")
        colors = list(red.range_to(Color("green"), 11))
        for i in range(len(colors)):
            color = []
            for x in colors[i].get_rgb():
                color.append(int(x * 255.))
            colors[i] = color

        for i, color in enumerate(cluster_sentiments):
            img = Image.new('RGB', (32, 32), tuple(colors[color]))
            imgDrawer = ImageDraw.Draw(img)
            img.save(self.CLUSTER_IMAGES_FILENAME.format(i))

        comments_clusters_df = pd.DataFrame(comments_clusters)
        comments_clusters_df.columns = ['comment_id', 'cluster_id']

        print(comments_clusters_df.head())

        comments_clusters_df.to_csv(self.COMMENTS_FILENAME, encoding='UTF-8')

    def _save_cluster(self, clusters):
        cluster_df = pd.DataFrame(clusters)
        cluster_df.columns = ['cluster_id', 'summary']

        print(cluster_df.head())

        cluster_df.to_csv(self.CLUSTERS_FILENAME, encoding='UTF-8')

    def _save_tags(self, tags):
        tags_df = pd.DataFrame(tags)
        tags_df.columns = ['tag_id', 'name']

        print(tags_df.head())

        tags_df.to_csv(self.TAGS_FILENAME, encoding='UTF-8')

    def _save_tag_comment(self, tag_comment):
        tag_comment_df = pd.DataFrame(tag_comment)
        tag_comment_df.columns = ['comment_id', 'tag_id']

        print(tag_comment_df.head())

        tag_comment_df.to_csv(self.TAGS_AND_COMMENTS, encoding='UTF-8')

    def _get_cluster_summaries(self, comments_clusters):
        clusters_with_summaries = dict()
        for i in range(self.num_of_clusters):
            if i not in clusters_with_summaries.keys():
                clusters_with_summaries[i] = {'post_ids': [],
                                              'summary': self.ERROR_NOT_ENOUGH_POSTS_FOR_SUMMARY,
                                              'keywords': [self.ERROR_NOT_ENOUGH_POSTS_FOR_TAGS]}

        for text_id, cluster_id in comments_clusters:
            clusters_with_summaries[cluster_id]['post_ids'].append(text_id)

        for cluster_id in clusters_with_summaries.keys():
            num_of_cluster_sentences = len(clusters_with_summaries[cluster_id]['post_ids'])
            if num_of_cluster_sentences < 10:
                continue

            random_text_from_cluster = '. '.join(self.corpus.texts[np.random.choice(num_of_cluster_sentences, 10)])

            clusters_with_summaries[cluster_id]['summary'] = summarize(random_text_from_cluster, word_count=150)

        cluster_summaries = []
        for i in range(self.num_of_clusters):
            cluster_summaries.append((i, clusters_with_summaries[i]['summary']))

        return cluster_summaries

    def _get_tags_from_cluster_summaries(self, cluster_summaries):
        summaries = []
        for cluster_id, cluster_summary in cluster_summaries:
            if cluster_summary == self.ERROR_NOT_ENOUGH_POSTS_FOR_TAGS:
                continue

            summaries.append(cluster_summary)

        summaries = [' '.join([word for word in text.lower().split() if word not in self.corpus.stop_words]) for text in
                     summaries]

        return list(enumerate(keywords('. '.join(summaries), split=True, words=15)))

    def _get_keywords_for_corpus(self):
        posts = []
        for text in DictionaryCreator().get_texts_clean(self.corpus.texts):
            posts.append('. '.join(text))

        posts = np.asarray(posts)
        num_of_corpus_sentences = len(posts)
        text_for_corpus = '. '.join(posts[np.random.choice(num_of_corpus_sentences, self.num_of_keywords_to_extract)])

        wordcloud = WordCloud(stopwords=self.corpus.stop_words)
        wordcloud.generate(text_for_corpus)
        image = wordcloud.to_image()
        image.save(self.CLUSTER_IMAGES_FILENAME.format('corpus'))

        return list(enumerate(keywords(text_for_corpus, split=True, words=self.num_of_keywords_to_extract)))

    def _get_tfidf_for_corpus(self):
        return models.TfidfModel(self.corpus.corpus, normalize=True)[self.corpus.corpus]

    def _get_frequencies_for_corpus(self):
        tf_vectorizer = CountVectorizer(max_df=0.6, min_df=10, max_features=1000, ngram_range=(1, 4),
                                        stop_words=self.corpus.stop_words)
        return tf_vectorizer.fit_transform(self.corpus.texts)

    def _get_model_LSI(self, tfidf_corpus):
        lsi = models.LdaModel(tfidf_corpus, id2word=self.corpus.dictionary, num_topics=self.num_of_clusters)
        return lsi[tfidf_corpus]

    def _get_model_LDA(self, corpus):
        # lda = models.LdaModel(corpus, id2word=self.corpus.dictionary, num_topics=5, alpha='auto', eval_every=50)
        lda = LatentDirichletAllocation(n_topics=self.num_of_clusters, max_iter=20,
                                        learning_method='online',
                                        learning_offset=50.,
                                        random_state=1)
        return lda.fit_transform(corpus)

    def _get_comments_clusters(self, corpus_model, model='artm'):
        comments_clusters = []

        if 'sklearn' == model:
            for i, doc in enumerate(corpus_model):
                comments_clusters.append((i, sorted(zip(range(len(doc)), doc), key=itemgetter(1), reverse=True)[0][0]))
        elif 'gensim' == model:
            for i, doc in enumerate(corpus_model):
                comments_clusters.append((i, sorted(doc, key=itemgetter(1), reverse=True)[0][0]))
        elif 'artm' == model:
            for i, doc in enumerate(corpus_model.values):
                comments_clusters.append((i, sorted(zip(range(len(doc)), doc), key=itemgetter(1), reverse=True)[0][0]))

        return comments_clusters

    def _get_tags_for_comments(self, tags):
        tag_comment = []
        for text_id, text in enumerate(self.corpus.texts):
            for tag_id, tag_name in tags:
                if text.find(tag_name) != -1:
                    tag_comment.append((text_id, tag_id))

        return tag_comment

    def _make_uci_dataset_from_corpus(self):
        num_of_doc = len(self.corpus.texts)

        # Count word frequences per document
        words_per_doc_freq = dict(enumerate([dict(Counter(x.lower().split())) for x in self.corpus.texts]))
        for k, v in words_per_doc_freq.items():
            words_per_doc_freq[k] = dict(v)

        # Count num of unique words
        unique_words = set()
        for text in self.corpus.texts:
            unique_words.update(text.split())

        unique_words = dict(zip(unique_words, range(1, len(unique_words) + 1)))
        num_of_unique_words = len(unique_words)

        # Count num of all words
        num_of_all_words = len(' '.join(self.corpus.texts).split(' '))

        self._write_docword_to_file(num_of_doc=num_of_doc,
                                    num_of_unique_words=num_of_unique_words,
                                    num_of_all_words=num_of_all_words,
                                    words_per_doc_freq=words_per_doc_freq,
                                    unique_words=unique_words)

        self._write_vocab_to_file(unique_words=unique_words)

    def _write_docword_to_file(self, num_of_doc, num_of_unique_words, num_of_all_words, words_per_doc_freq,
                               unique_words):
        with open(os.path.join(self.RESOURCES_FOLDER, 'docword.comm.txt'), 'w') as f:
            f.write(str(num_of_doc))
            f.write('\n')
            f.write(str(num_of_unique_words))
            f.write('\n')
            f.write(str(num_of_all_words))
            f.write('\n')

            for file_index in words_per_doc_freq.keys():
                freq_for_doc = words_per_doc_freq[file_index]

                for word in freq_for_doc.keys():
                    f.write(str(file_index + 1))
                    f.write(' ')
                    f.write(str(unique_words[word]))
                    f.write(' ')
                    f.write(str(freq_for_doc[word]))
                    f.write('\n')

    def _write_vocab_to_file(self, unique_words):
        with open(os.path.join(self.RESOURCES_FOLDER, 'vocab.comm.txt'), 'w') as f:
            for key, v in unique_words.items():
                f.write(key)
                f.write('\n')


if __name__ == '__main__':
    cleaner = DatasetCleaner(csv_path='../neg_comments_t_50000.csv')
    plain_publications = cleaner.clean_texts_from_junk()

    dictionary = DictionaryCreator().create_dictionary_from_texts(' '.join(plain_publications))

    corpus = CorpusCreator(plain_publications, sentiments=cleaner.get_sentiments_for_texts(), dictionary=dictionary)

    cth = ClusterTopicsHelper(corpus)
    cth.cluster_texts()
