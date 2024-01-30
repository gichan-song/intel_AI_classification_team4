import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

from konlpy.tag import Okt

from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.utils import to_categorical

import pickle

from tensorflow.keras.models import load_model

df = pd.read_csv("../naver_economy/naver_test_headline_news_20240130.csv")
print(df.head())
print(df.info())

X = df["titles"]
Y = df["category"]

with open("../naver_economy/label_encoder.pickle", "rb") as file:
    label_encoder = pickle.load(file)

label = label_encoder.classes_

print(label)

okt = Okt()

for i in range(len(X)):
    X[i] = okt.morphs(X[i], stem = True)

stopwords = pd.read_csv("./stopwords.csv")

for i in range(len(X)):
    words = []
    for j in range(len(X[i])):
        if len(X[i][j]) > 1:
            if X[i][j] not in list(stopwords["stopword"]):
                words.append(X[i][j])

    X[i] = " ".join(words)

with open("../naver_economy/news_token.pickle", "rb") as file:
    token = pickle.load(file)

tokened_x = token.texts_to_sequences(X)

for i in range(len(tokened_x)):
    if len(tokened_x[i]) > 20:
        tokened_x[i] = tokened_x[i][:20]

print(tokened_x)

x_pad = pad_sequences(tokened_x, 20)

model = load_model("../naver_economy/economy_category_classification_model_0.5552995204925537.h5")

preds = model.predict(x_pad)

predicts = []

for pred in preds:
    most = label[np.argmax(pred)]
    pred[np.argmax(pred)] = 0
    second = label[np.argmax(pred)]
    predicts.append([most, second])

df["predict"] = predicts

print(df)


df["OX"] = 0

for i in range(len(df)):
    if df.loc[i, "category"] in df.loc[i, "predict"]:
        df.loc[i, "OX"] = "O"
    else:
        df.loc[i, "OX"] = "X"

print(df["OX"].value_counts())

print(df["OX"].value_counts() / len(df))


