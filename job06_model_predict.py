import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from konlpy.tag import Okt
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.utils import to_categorical
import pickle
from tensorflow.keras.models import load_model



df = pd.read_csv('./crawling_data/test.csv')
print(df.head())
df.info()

X = df['titles']
Y = df['category']

with open('./models/encoder.pickle', 'rb') as f:
    encoder = pickle.load(f)
labeled_y = encoder.transform(Y)        # fit 사용하지 않음, 새로운 encorder가 아닌 기존의 것을 사용하기 때문
label = encoder.classes_

onehot_y = to_categorical(labeled_y)
print(onehot_y)

okt = Okt()

for i in range(len(X)):
    X[i] = okt.morphs(X[i], stem=True)
stopwords = pd.read_csv('./stopwords.csv', index_col=0)

for j in range(len(X)):
    words = []
    for i in range(len(X[j])):
        if len(X[j][i]) > 1:
            if X[j][i] not in list(stopwords['stopword']):
                words.append(X[j][i])
    X[j] = ' '.join(words)

with open('./models/book_token.pickle', 'rb') as f:
    token = pickle.load(f)
tokened_x = token.texts_to_sequences(X)
for i in range(len(tokened_x)):
    if len(tokened_x[i]) > 21:
        tokened_x[i] = tokened_x[i][:22]
x_pad = pad_sequences(tokened_x, 21)

model = load_model('./models/book_titles_classification_model_0.5230213403701782.h5')
preds = model.predict(x_pad)
predicts = []
for pred in preds:
    most = label[np.argmax(pred)]
    pred[np.argmax(pred)] = 0
    second = label[np.argmax(pred)]
    predicts.append([most, second])
df['predict'] = predicts
print(df)

df['OX'] = 0
for i in range(len(df)):
    if df.loc[i, 'category'] in df.loc[i, 'predict']:
        df.loc[i, 'OX'] = '0'
    else:
        df.loc[i, 'OX'] = 'X'
print(df['OX'].value_counts())
print(df['OX'].value_counts()/len(df))
for i in range(len(df)):
    if df['category'][i] not in df['predict'][i]:
        print(df.iloc[i])











