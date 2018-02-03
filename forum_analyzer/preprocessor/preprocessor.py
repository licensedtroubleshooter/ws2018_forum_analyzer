import os
import forum_analyzer.preprocessor.groups_parser as pg
import forum_analyzer.preprocessor.cluster as clustering
from forum_analyzer.preprocessor.trash_preprocessor import trash_preprocessing as tp
from forum_analyzer.preprocessor.sentiment_preprocessor import sentiment_preprocessing as sa


def preprocessed_group(link):
    path = os.path.join(os.path.dirname(__file__), "resources")
    processed_comments = sa.sentiment_analysis(path=path,
                                               train=tp.cleaning_comments(pg.save_comments_to_csv(link.replace(' ', ''),
                                                                                                  path),
                                                                          path))
    # processed_comments = '/home/rebcd/Education/Git/ws18_web_interface/forum_analyzer/preprocessor/resources/neg_pos_comments31.csv'

    print('start clusterization and extract tags')

    cleaner = clustering.DatasetCleaner(csv_path=processed_comments)
    plain_publications = cleaner.clean_texts_from_junk()

    dictionary = clustering.DictionaryCreator().create_dictionary_from_texts(plain_publications)

    corpus = clustering.CorpusCreator(plain_publications, dictionary)

    cth = clustering.ClusterTopicsHelper(corpus)
    cth.cluster_texts()

    print('stop clusterization and extract tags')

    return True


def main():
    link = input('Input link to groups: ')
    comments = pg.save_comments_to_csv(link[:-1])
    # comments = '/home/rebcd/Education/Git/ws18_web_interface/forum_analyzer/raw_comments.csv'
    print(comments)
    comments = tp.cleaning_comments(comments)
    print(comments)
    comments = sa.sentiment_analysis(comments)
    print(comments)


if __name__ == '__main__':
    main()