import re
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

import pandas as pd
import numpy as np

from tagging.tag import TagDatasetHelper
from summarization.summary import SummarizeTextHelper


def get_twitter_dataset():
    df = pd.read_csv('data/negative.csv', sep=';')
    df = df.iloc[:, [3, 4]]

    df.columns = ['plain_text', 'sentiment']
    plain_publications = [text.strip().lower() for text in df['plain_text'].tolist()]

    for i, publication in enumerate(plain_publications):
        plain_publications[i] = ' '.join(list(filter(None, re.split('[^а-я]', publication))))

    return np.asarray(plain_publications)


if __name__ == '__main__':
    plain_publications = get_twitter_dataset()

    # extract tags from text
    tags_with_posts = TagDatasetHelper().get_tags_with_posts(plain_publications)
    print(list(tags_with_posts.items())[:10])

    # summarize text per tag
    tags_with_summarized_posts = SummarizeTextHelper().summarize_text_per_tag(tags_with_posts, plain_publications)
    print(tags_with_summarized_posts)
