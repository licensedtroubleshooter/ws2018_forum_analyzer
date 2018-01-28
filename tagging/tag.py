import re
import nltk
import operator


class TagDatasetHelper(object):
    def __init__(self):
        nltk.download('stopwords')
        self.words_occurrences = None
        self.publications = None
        self.tag_publications = None

    def count_words_occurrences(self, publications, n=100):
        self.publications = publications
        stop = set(nltk.corpus.stopwords.words('russian'))

        words_occurrences = dict()
        for text in publications:
            for word in list(filter(None, re.split('[^а-я]', text))):
                if word in stop:
                    continue

                if word not in words_occurrences.keys():
                    words_occurrences[word] = 0
                words_occurrences[word] += 1

        self.words_occurrences = sorted(words_occurrences.items(), key=operator.itemgetter(1), reverse=True)
        return self.words_occurrences[:n]

    def get_posts_for_tags(self, tags):
        tag_publications = dict()
        for tag, _ in tags:
            tag_publications[tag] = []

        for i, text in enumerate(self.publications):
            for tag in tag_publications.keys():
                if text.find(tag) >= 0:
                    tag_publications[tag].append(i)

        self.tag_publications = tag_publications
        return self.tag_publications
