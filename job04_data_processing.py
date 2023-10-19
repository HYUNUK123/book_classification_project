import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from konlpy.tag import Okt
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.utils import to_categorical
import pickle

pd.set_option('display.unicode.east_asian_width', True)
df = pd.read_csv('./crawling_data/*.csv')

X = df['contents']
Y = df['titles']

encoder = LabelEncoder()
labeled_y = encoder.fit_transform(Y)
label = encoder.classes_

with open('./models/encoder.pickle', 'wb') as f:
    pickle.dump(encoder, f)

onehot_y = to_categorical(labeled_y)

okt = Okt()

for i in range(len(X)):
    X[i] = okt.morphs(X[i], stem=True)

stopwords = pd.read_csv('./stopwords.csv', index_col=0)
for j in range(len(X)):
    words = []
    for i in range(len(X[j])):
        if len(X[j][i]) >1 :
            if X[j][i] not in list(stopwords['stopword']):
                words.append(X[j][i])
    X[j] = ' '.join(words)

token = Tokenizer()
token.fit_on_texts(X)
tokened_x = token.texts_to_sequences(X)
wordsize = len(token.word_index) +1

with open('./models/book_token.pickle', 'wb') as f:
    pickle.dump(token, f)

max = 0
for i in range(len(tokened_x)):
    if max < len(tokened_x[i]):
        max = len(tokened_x[i])

x_pad = pad_sequences(tokened_x, max)

X_train, X_test, Y_train, Y_test = train_test_split(
    x_pad, onehot_y, test_size = 0.2
)

xy = X_train, X_test, Y_train, Y_test
np.save('./crawling_data/book_data_max_{}_wordsize_{}'.format(max,wordsize), xy)

