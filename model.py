import random
import pickle
import heapq
import numpy as np
import pandas as pd
from nltk.tokenize import RegexpTokenizer
import tensorflow as tf

from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import LSTM, Dense, Activation
from tensorflow.keras import optimizers

text_df = pd.read_csv("fake_or_real_news.csv")
text = text_df.text.values.tolist()
joined_text = " ".join(text)
partial_text = joined_text[:10000]

tokenizer = RegexpTokenizer(r"\w+")
tokens = tokenizer.tokenize(partial_text.lower())

unique_tokens = np.unique(tokens)
unique_token_index = {token: idx for idx, token in enumerate(unique_tokens)}

n_words = 10
input_words = []
next_words = []

for i in range(len(tokens) - n_words):
    input_words.append(tokens[i:i + n_words])
    next_words.append(tokens[i + n_words])

X = np.zeros((len(input_words), n_words, len(unique_tokens)), dtype=float)
Y = np.zeros((len(next_words), len(unique_tokens)), dtype=float)

for i, words in enumerate(input_words):
    for j, word in enumerate(words):
        X[i, j, unique_token_index[word]] = 1
    Y[i, unique_token_index[next_words[i]]] = 1

model = Sequential()
model.add(LSTM(128, input_shape=(n_words, len(unique_tokens)), return_sequences=True))
model.add(LSTM(128))
model.add(Dense(len(unique_tokens)))
model.add(Activation("softmax"))

model.compile(loss="categorical_crossentropy", optimizer=optimizers.RMSprop(learning_rate=.01), metrics=["accuracy"])
history = model.fit(X, Y, batch_size=128, epochs=30, shuffle=True).history
#history = model.fit(X, y, batch_size=128, epochs=5, shuffle=True).history
model.save("model.h5")
with open("history2.p", "wb") as f:
    pickle.dump(history, f)
model = load_model("model.h5")
history = pickle.load(open("history2.p", "rb"))

def predict_next_word(input_text, n_best):
    input_text = input_text.lower()
    X = np.zeros((1, n_words, len(unique_tokens)))
    for j, word in enumerate(input_text.split()):
        X[0, j, unique_token_index[word]] = 1
    predictions = model.predict(X)[0]
    return np.argpartition(predictions, -n_best)[-n_best:]


possible = predict_next_word("He will have to look into this thing and he", 5)

#print([unique_tokens[idx] for idx in possible])

def generate_text(input_text, n_words, creativity=3):
    word_sequence = input_text.split()
    current = 0
    for _ in range(n_words):
        sub_sequence = " ".join(tokenizer.tokenize(" ".join(word_sequence).lower())[current:current+n_words])
        try:
            choice = unique_tokens[random.choice(predict_next_word(sub_sequence, creativity))]
        except:
            choice = random.choice(unique_tokens)
        word_sequence.append(choice)
        current += 1
    return choice