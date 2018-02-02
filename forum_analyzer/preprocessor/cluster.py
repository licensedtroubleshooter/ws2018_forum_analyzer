import os
# import artm
import re
import pymystem3
from operator import itemgetter

import numpy as np
import pandas as pd

from collections import Counter, defaultdict
from gensim import corpora, models
from gensim.summarization import summarize, keywords
from nltk.corpus import stopwords


class DatasetCleaner(object):
    def __init__(self, csv_path):
        self.texts = pd.read_csv(csv_path)['text'].tolist()

    def clean_texts_from_junk(self):
        plain_publications = [text.strip().lower() for text in self.texts]
        for i, publication in enumerate(plain_publications):
            plain_publications[i] = ' '.join(list(filter(None, re.split('[^а-я]', publication))))

        return plain_publications


class DictionaryCreator(object):
    def __init__(self):
        self.stop_words = set(stopwords.words('russian'))

    def create_dictionary_from_texts(self, texts):
        texts = self._remove_stop_words(texts)
        texts = self._remove_words_that_appear_only_once(texts)
        texts = self._lemmatize_words(texts)

        return self._create_and_save_dictionary(texts)

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
    COMMENTS_DICT_FILE_NAME = os.path.join(PATH, 'resources', "comments.dict")
    COMMENTS_MM_FILE_NAME = os.path.join(PATH, 'resources', "comments.mm")

    def __init__(self, texts, dictionary=None):
        if (os.path.exists(self.COMMENTS_DICT_FILE_NAME) and os.path.exists(self.COMMENTS_MM_FILE_NAME)):
            self.dictionary = corpora.Dictionary.load(self.COMMENTS_DICT_FILE_NAME)
            self.corpus = corpora.MmCorpus(self.COMMENTS_MM_FILE_NAME)
        else:
            self.dictionary = dictionary
            self.corpus = [self.dictionary.doc2bow([token for token in text]) for text in texts]

            corpora.MmCorpus.serialize(self.COMMENTS_MM_FILE_NAME, self.corpus)

        self.texts = np.asarray(texts)

class ClusterTopicsHelper(object):
    PATH = os.path.dirname(__file__)
    CLUSTERS_FILENAME = os.path.join(PATH, 'resources', 'clusters.csv')
    TAGS_FILENAME = os.path.join(PATH, 'resources', 'tags.csv')
    COMMENTS_FILENAME = os.path.join(PATH, 'resources', 'comments.csv')
    TAGS_AND_COMMENTS = os.path.join(PATH, 'resources', 'tags_comments.csv')

    ERROR_NOT_ENOUGH_POSTS_FOR_SUMMARY = 'Summary is not available for this cluster.'
    ERROR_NOT_ENOUGH_POSTS_FOR_TAGS = 'Keywords are not available for this cluster.'

    def __init__(self, corpus):
        self.corpus = corpus
        self.num_of_clusters = 5

    def cluster_texts(self, method='LDA'):
        corpus_vector_spaced = self._get_tfidf_for_corpus()

        if 'LSI' == method:
            corpus_modeled = self._get_model_LSI(corpus_vector_spaced)
        else:
            corpus_modeled = self._get_model_LDA(corpus_vector_spaced)

        comments_clusters = self._get_comments_clusters(corpus_modeled)
        self._save_comments(comments_clusters)

        cluster_summaries = self._get_cluster_summaries(comments_clusters)
        self._save_cluster(cluster_summaries)

        tags = self._get_tags_from_cluster_summaries(cluster_summaries)
        self._save_tags(tags)

        tag_comment = self._get_tags_for_comments(tags)
        self._save_tag_comment(tag_comment)

    def _save_comments(self, comments_clusters):
        comments_clusters_df = pd.DataFrame(comments_clusters)
        comments_clusters_df.columns = ['comment_id', 'cluster_id']

        print(comments_clusters_df.head())

        comments_clusters_df.to_csv(self.COMMENTS_FILENAME, encoding='UTF-8')

    def _save_cluster(self, cluster):
        cluster_df = pd.DataFrame(cluster)
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

        return list(enumerate(keywords(' '.join(summaries), split=True, words=15)))

    def _get_tfidf_for_corpus(self):
        return models.TfidfModel(self.corpus.corpus, normalize=True)[self.corpus.corpus]

    def _get_model_LSI(self, tfidf_corpus):
        lsi = models.LdaModel(tfidf_corpus, id2word=self.corpus.dictionary, num_topics=5)
        return lsi[tfidf_corpus]

    def _get_model_LDA(self, corpus):
        lda = models.LdaModel(corpus, id2word=self.corpus.dictionary, num_topics=5)
        return lda[corpus]

    def _get_comments_clusters(self, corpus_model):
        comments_clusters = []
        for i, doc in enumerate(corpus_model):
            comments_clusters.append((i, sorted(doc, key=itemgetter(1), reverse=True)[0][0]))

        return comments_clusters

    def _get_tags_for_comments(self, tags):
        tag_comment = []
        for text_id, text in enumerate(self.corpus.texts):
            for tag_id, tag_name in tags:
                if text.find(tag_name) != -1:
                    tag_comment.append((text_id, tag_id))

        return tag_comment

    def _make_uci_dataset_from_csv(self):
        def clean_data(df):
            plain_publications = [text.strip().lower() for text in df['text'].tolist()]
            for i, publication in enumerate(plain_publications):
                plain_publications[i] = ' '.join(list(filter(None, re.split('[^а-я]', publication))))

            return plain_publications

        self.df['text'] = clean_data(self.df)
        num_of_doc = self.df.shape[0]

        # Count word frequenses per document
        words_per_doc_freq = dict(self.df['text'].apply(lambda x: Counter(x.lower().split())))
        for k, v in words_per_doc_freq.items():
            words_per_doc_freq[k] = dict(v)

        # Count num of unique words
        unique_words = set()
        self.df['text'].str.lower().str.split().apply(unique_words.update)
        unique_words = dict(zip(unique_words, range(1, len(unique_words) + 1)))
        num_of_unique_words = len(unique_words)

        # Count num of all words
        num_of_all_words = len(' '.join(self.df['text'].tolist()).split(' '))

        self._write_docword_to_file(num_of_doc=num_of_doc,
                                    num_of_unique_words=num_of_unique_words,
                                    num_of_all_words=num_of_all_words,
                                    words_per_doc_freq=words_per_doc_freq,
                                    unique_words=unique_words)

        self._write_vocab_to_file(unique_words=unique_words)

    def _write_docword_to_file(self, num_of_doc, num_of_unique_words, num_of_all_words, words_per_doc_freq, unique_words):
        with open('docword.corpus.txt', 'w') as f:
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
        with open('vocab.corpus.txt', 'w') as f:
            for key, v in unique_words.items():
                f.write(key)
                f.write('\n')


if __name__ == '__main__':
    cleaner = DatasetCleaner(csv_path='../neg_comments_t_50000.csv')
    plain_publications = cleaner.clean_texts_from_junk()

    dictionary = DictionaryCreator().create_dictionary_from_texts(plain_publications)

    corpus = CorpusCreator(plain_publications, dictionary)

    cth = ClusterTopicsHelper(corpus)
    cth.cluster_texts()
