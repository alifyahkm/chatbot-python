# importing the libraries
import random
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.preprocessing.sequence import pad_sequences
import string
import tensorflow as tf
import numpy as np
import pandas as pd
import json
import nltk
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.layers import Input, Embedding, LSTM, Dense, GlobalMaxPooling1D, Flatten
from tensorflow.keras.models import Model
import matplotlib.pyplot as plt

# memuat dataset
with open('content.json') as content:
    data1 = json.load(content)
# memasukkan setiap data dalam json kebentuk list
tags = []
inputs = []
responses = {}
for intent in data1['intents']:
    responses[intent['tag']] = intent['responses']
    for lines in intent['input']:
        inputs.append(lines)
        tags.append(intent['tag'])
# mengubah bentuk data dari json ke dataframe pandas
data = pd.DataFrame({"inputs": inputs,
                     "tags": tags})
print(data)

# menghapus tanda baca
data['inputs'] = data['inputs'].apply(
    lambda wrd: [ltrs.lower() for ltrs in wrd if ltrs not in string.punctuation])
data['inputs'] = data['inputs'].apply(lambda wrd: ''.join(wrd))
# melakukan tokenizing pada data input
tokenizer = Tokenizer(num_words=2000)
tokenizer.fit_on_texts(data['inputs'])
train = tokenizer.texts_to_sequences(data['inputs'])

# menambahkan padding sequences pada data x_train
x_train = pad_sequences(train)

# melakukan encoding atau merubah tag menjadi angka
le = LabelEncoder()
y_train = le.fit_transform(data['tags'])

# mengambil ukuran data input
input_shape = x_train.shape[1]
print(input_shape)
# mendefinisikan kosa kata yang unik
vocabulary = len(tokenizer.word_index)
print("number of unique words : ", vocabulary)
# mengambil ukuran data output
output_length = le.classes_.shape[0]
print("output length: ", output_length)

# membentuk model neural network
i = Input(shape=(input_shape,))
x = Embedding(vocabulary+1, 10)(i)
x = LSTM(10, return_sequences=True)(x)
x = Flatten()(x)
x = Dense(output_length, activation="softmax")(x)
model = Model(i, x)
# melakukan kompilasi pada model
model.compile(loss="sparse_categorical_crossentropy",
              optimizer='adam', metrics=['accuracy'])
# melakukan training dengan model yang sudah dibentuk
train = model.fit(x_train, y_train, epochs=500, batch_size=25, verbose=1)


def response_to_chat(prediction_input):
 # menghapus tanda baca dan mengubah ke huruf kecil semua
    texts_p = []
    prediction_input = [letters.lower(
    ) for letters in prediction_input if letters not in string.punctuation]
    prediction_input = ''.join(prediction_input)
    texts_p.append(prediction_input)
    #tokenizing and padding
    prediction_input = tokenizer.texts_to_sequences(texts_p)
    prediction_input = np.array(prediction_input).reshape(-1)
    prediction_input = pad_sequences([prediction_input], input_shape)
    # mengambil output dari model yang sudah di train
    output = model.predict(prediction_input)
    print(f"Predict :{output}")
    output = output.argmax()
    print(f"Argmax:{output}")
    # mencari tag sesuai hasil dari model
    response_tag = le.inverse_transform([output])[0]
    return random.choice(responses[response_tag])


# chatting
# while True:

#   prediction_input = input('You : ')
#   print(f"Response : {response_to_chat(prediction_input)}")
