import pandas as pd
from sklearn.externals import joblib

model, count_vect = joblib.load('predictor_stop_clear')

def WriteToCSV(df, neg_ar, pos_ar):
    new_df_neg = pd.DataFrame()
    new_df_pos = pd.DataFrame()
    
    for i in range(0,len(neg_ar)):
        new_df_neg = new_df_neg.append(df.loc[neg_ar[i]])
    new_df_neg['sentiment'] = 0
                    
    for j in range(0,len(pos_ar)):
        new_df_pos = new_df_pos.append(df.loc[pos_ar[j]])
    new_df_pos['sentiment'] = 1

    frames = [new_df_neg, new_df_pos]
    df_all = pd.concat(frames)
    
    df_all.to_csv('neg_pos_comments31.csv', index = False)
    
   
def SentimentAnalysis():
    df = pd.read_csv('sushiwok.csv')
    a_neg = []
    a_pos = []
    for i in range(0,len(df)):
        sem_an = model.predict(count_vect.transform([df['text'].loc[i]]))
        if sem_an < 0.4:
            a_neg.append(i)
        if sem_an > 1:
            a_pos.append(i)
            
    WriteToCSV(df, a_neg, a_pos)

def main():
    SentimentAnalysis()

if __name__ == '__main__':
    main()