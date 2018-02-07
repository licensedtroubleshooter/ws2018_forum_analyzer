import os
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import Ridge
from sklearn.externals import joblib

class SentimentAnalysis(object):
    def __init__(self, root_path='./data'):
        self.DATA_ROOT_PATH = root_path
        self.TRAIN_DATASET_PATH = os.path.join(self.DATA_ROOT_PATH, 'twitter_clean.csv')
        self.STOP_WORDS_PATH = os.path.join(self.DATA_ROOT_PATH, 'swords.txt')
        self.SENTIMENT_MODEL_PATH = os.path.join(self.DATA_ROOT_PATH, 'predictor_stop_wng_md_clear')


    def train_preprocessor(self):
        print('start train sentiment preprocessor...')
        df = pd.read_csv(self.TRAIN_DATASET_PATH)
        df.columns = ['id', 'text', 'sent']

        df_n = df['text'][:-114910]
        df_p = df['text'][111923:]

        df_n = df_n.dropna(axis=0, how='all')
        df_p = df_p.dropna(axis=0, how='all')

        frames = [df_n, df_p]
        train = pd.concat(frames)

        y = []
        for i in range(0, len(df_n)):
            y.append(0)
        for i in range(0, len(df_p)):
            y.append(1)

        # -*- coding: iso-8859-5 -*-
        with open(self.STOP_WORDS_PATH) as file:
            sw = [row.strip() for row in file]

        ngram = (1, 3)

        count_vect = CountVectorizer(stop_words=sw, max_df=0.5, ngram_range=ngram)

        X_train_counts = count_vect.fit_transform(train)

        count_vect.get_feature_names()

        model = Ridge(alpha=1)
        model.fit(X_train_counts, y)

        joblib.dump((model, count_vect), self.SENTIMENT_MODEL_PATH)
        print('end train sentiment preprocessor...')


    def write_to_csv(self, df, neg_ar, pos_ar, sem_neg, sem_pos):
        new_df_neg = pd.DataFrame()
        new_df_pos = pd.DataFrame()

        sem_n = pd.Series(sem_neg)
        sem_p = pd.Series(sem_pos)

        for i in range(0, len(neg_ar)):
            new_df_neg = new_df_neg.append(df.loc[neg_ar[i]])

        new_df_neg['color'] = 0
        new_df_neg['sentiment'] = sem_n.values
        for j in range(0, len(pos_ar)):
            new_df_pos = new_df_pos.append(df.loc[pos_ar[j]])
        new_df_pos['color'] = 1
        new_df_pos['sentiment'] = sem_p.values

        frames = [new_df_neg, new_df_pos]
        df_all = pd.concat(frames)

        df_all['likes'] = df_all['likes'].astype(int)
        df_all['status'] = df_all['status'].astype(int)

        df_all.to_csv(os.path.join(self.DATA_ROOT_PATH, 'neg_pos_comments31.csv'), index=False)

        return os.path.join(self.DATA_ROOT_PATH, 'neg_pos_comments31.csv')

    def sentiment_analysis(self, train='train.csv'):
        print('analyze tonality of comments...')

        model, count_vect = joblib.load(os.path.join(self.DATA_ROOT_PATH, 'predictor_stop_wng_md_clear'))
        df = pd.read_csv(train)
        a_neg = []
        a_pos = []
        sem_neg = []
        sem_pos = []
        for i in range(0, len(df)):
            sem_an = model.predict(count_vect.transform([df['text'].loc[i]]))
            if sem_an < 0.4:
                a_neg.append(i)
                sem_neg.append(float(sem_an))
            if sem_an > 1.5:
                a_pos.append(i)
                sem_pos.append(float(sem_an))

        os.remove(train)

        return self.write_to_csv(df, a_neg, a_pos, sem_neg, sem_pos)


def main():
    sentiment = SentimentAnalysis()
    #sentiment.train_preprocessor()
    sentiment.sentiment_analysis()


if __name__ == '__main__':
    main()