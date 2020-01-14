from __future__ import print_function

import csv
import random

import numpy as np
from keras.layers import Conv1D, GlobalMaxPooling1D
from keras.layers import Dense, Dropout, Activation
from keras.layers import Embedding
from keras.models import Sequential
from keras.preprocessing import sequence
from keras.preprocessing.text import Tokenizer

with open('wines_final.csv', newline='', encoding='utf-8') as file:
    reader = csv.DictReader(file, delimiter=';')
    rows = [row for row in reader]

dataset = [(row['description'], 0) for row in rows]

with open('beers_final.csv', newline='', encoding='utf-8') as file:
    reader = csv.DictReader(file, delimiter=';')
    rows = [row for row in reader]

dataset = dataset + [(row['review'], 1) for row in rows]

random.shuffle(dataset)

t = Tokenizer(num_words=7000)
texts = [text[0] for text in dataset]
t.fit_on_texts(texts)

dataset_processed = [(x, y) for (x, y) in zip(t.texts_to_sequences(texts), (entry[1] for entry in dataset))]
# print(len(dataset_processed))

dataset_size = len(dataset_processed)
train, test = dataset_processed[:dataset_size // 2], dataset_processed[dataset_size // 2:]

# print("Train size:", len(train))
# print("Test size:", len(test))

x_train, y_train = np.array([x[0] for x in train]), np.array([x[1] for x in train]).astype(int)
x_test, y_test = np.array([x[0] for x in test]), np.array([x[1] for x in test]).astype(int)

# set parameters:
max_features = 7000
maxlen = 400
batch_size = 32
embedding_dims = 50
filters = 250
kernel_size = 3
hidden_dims = 250
epochs = 2

# print(x_train[0])
# print(y_train[0])

# print('Loading data...')
# (x_train, y_train), (x_test, y_test) = imdb.load_data(num_words=max_features)
print(x_train)
print(y_train)
print(len(x_train), 'train sequences')
print(len(x_test), 'test sequences')

print('Pad sequences (samples x time)')
x_train = sequence.pad_sequences(x_train, maxlen=maxlen)
x_test = sequence.pad_sequences(x_test, maxlen=maxlen)
print('x_train shape:', x_train.shape)
print('x_test shape:', x_test.shape)
#
print('Build model...')
model = Sequential()

# we start off with an efficient embedding layer which maps
# our vocab indices into embedding_dims dimensions
model.add(Embedding(max_features,
                    embedding_dims,
                    input_length=maxlen))
model.add(Dropout(0.2))
#
# we add a Convolution1D, which will learn filters
# word group filters of size filter_length:
model.add(Conv1D(filters,
                 kernel_size,
                 padding='valid',
                 activation='relu',
                 strides=1))
# we use max pooling:
model.add(GlobalMaxPooling1D())
#
# We add a vanilla hidden layer:
model.add(Dense(hidden_dims))
model.add(Dropout(0.2))
model.add(Activation('relu'))
#
# We project onto a single unit output layer, and squash it with a sigmoid:
model.add(Dense(1))
model.add(Activation('sigmoid'))
#
model.compile(loss='binary_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])
model.fit(x_train, y_train,
          batch_size=batch_size,
          epochs=epochs,
          validation_data=(x_test, y_test))
