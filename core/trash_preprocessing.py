# import numpy as np
import os
import pandas as pd
from catboost import CatBoostClassifier
from sklearn.externals import joblib
from sklearn.feature_extraction.text import CountVectorizer


class Cleaner(object):
    def __init__(self, root_path='./data'):
        self.DATA_ROOT_PATH = root_path


    def train_preprocessor(self, train='train.csv'):
        print('start train trash preprocessor...')
        df = pd.read_csv(os.path.join(self.DATA_ROOT_PATH, train))

        train_data = df[:-100]
        validation_data = df[-100: -50]

        vectorizer = CountVectorizer()
        x_train_counts = vectorizer.fit_transform(train_data.text)
        x_validation_counts = vectorizer.transform(validation_data.text)

        model = CatBoostClassifier(iterations=250,
                                   train_dir=self.DATA_ROOT_PATH,
                                   logging_level='Silent',
                                   allow_writing_files=False)

        model.fit(X=x_train_counts.toarray(),
                  y=train_data.status,
                  eval_set=(x_validation_counts.toarray(), validation_data.status),
                  use_best_model=True,)

        model.save_model(os.path.join(self.DATA_ROOT_PATH, 'trash_model'))
        joblib.dump(vectorizer,os.path.join(self.DATA_ROOT_PATH, 'trash_vectorizer'))

        print('end train sentiment preprocessor...')


    def cleaning_comments(self, raw_comments, path='.') -> str:
        print('start cleaning of comments...')

        raw = pd.read_csv(raw_comments)
        cleaned_comments = os.path.join(path, 'cleaned_comments.csv')
        bad_comments = os.path.join(path, 'bad_comments.csv')

        model = CatBoostClassifier().load_model(os.path.join(path, 'trash_model'))
        vectorizer = joblib.load(os.path.join(path, 'trash_vectorizer'))

        hyp = model.predict_proba(vectorizer.transform(raw.text).toarray())
        with open(cleaned_comments, 'w') as cleaned, open(bad_comments, 'w') as bad:
            bad_file = 'likes,status,text\n'
            cleaned_file = 'likes,status,text\n'
            for i in range(len(hyp)):
                if hyp[i][0] < 0.6:
                    bad_file += str(raw.likes[i]) + ',1,"' + raw.text[i] + '"\n'
                else:
                    cleaned_file += str(raw.likes[i]) + ',0,"' + raw.text[i] + '"\n'
            cleaned.write(cleaned_file)
            bad.write(bad_file)

        os.remove(raw_comments)

        print('end cleaning of comments...')
        return cleaned_comments


def main():
    train_preprocessor('train.csv')
    cleaning_comments('rc.csv')


if __name__ == '__main__':
    main()