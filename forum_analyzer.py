import pandas as pd

from tagging.tag import TagDatasetHelper


def get_twitter_dataset():
    df = pd.read_csv('data/negative.csv', sep=';')
    df = df.iloc[:, [3, 4]]

    df.columns = ['plain_text', 'sentiment']
    return df


if __name__ == '__main__':
    df = get_twitter_dataset()
    plain_publications = [text.strip().lower() for text in df['plain_text'].tolist()]

    tag_dataset_helper = TagDatasetHelper()
    tags = tag_dataset_helper.count_words_occurrences(plain_publications)
    sentences_for_tags = tag_dataset_helper.get_posts_for_tags(tags)

    for sentence_index in sentences_for_tags['мама']:
        print(plain_publications[sentence_index])