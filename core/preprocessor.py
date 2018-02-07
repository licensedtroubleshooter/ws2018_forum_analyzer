import os

import core.cluster as clustering
import core.groups_parser as pg
from core import trash_preprocessing as tp, sentiment_preprocessing as sa


def preprocessed_group(link):
    path = os.path.join(os.path.dirname(__file__), "../forum_analyzer/preprocessor/resources")
    processed_comments = sa.sentiment_analysis(path=path,
                                               train=tp.cleaning_comments(
                                                   pg.save_comments_to_csv(link.replace(' ', ''), path), path))
    # processed_comments = '/home/rebcd/Education/Git/ws18_web_interface/forum_analyzer/preprocessor/resources/neg_pos_comments31.csv'

    print('start clusterization and extract tags')

    cleaner = clustering.DatasetCleaner(csv_path=processed_comments)
    plain_publications = cleaner.clean_texts_from_junk()

    dictionary = clustering.DictionaryCreator().create_dictionary_from_texts(plain_publications)

    corpus = clustering.CorpusCreator(plain_publications, cleaner.get_sentiments_for_texts(), dictionary)

    cth = clustering.ClusterTopicsHelper(corpus)
    cth.cluster_texts()

    print('stop clusterization and extract tags')

    return True


def main():
    link = input('Input link to groups: ')

    parser = pg.Parser()
    comments = parser.save_comments_to_csv('https://vk.com/planetasushi_ru')
    #comments = pg.save_comments_to_csv(link[:-1])
    print(comments)

    cleaner = tp.Cleaner()
    comments = cleaner.cleaning_comments(comments)
    print(comments)

    sentiment_analyzer = sa.SentimentAnalysis()
    comments = sentiment_analyzer.sentiment_analysis(comments)
    print(comments)

    print('start clusterization and extract tags')

    cleaner = clustering.DatasetCleaner(csv_path=comments)
    plain_publications = cleaner.clean_texts_from_junk()

    dictionary = clustering.DictionaryCreator().create_dictionary_from_texts(plain_publications)

    corpus = clustering.CorpusCreator(plain_publications, cleaner.get_sentiments_for_texts(), dictionary)

    cth = clustering.ClusterTopicsHelper(corpus)
    cth.cluster_texts()

    print('stop clusterization and extract tags')


if __name__ == '__main__':
    main()