from __future__ import print_function

import csv
from ast import literal_eval

import numpy as np
from keras.layers import Conv1D, GlobalMaxPooling1D
from keras.layers import Dense, Dropout, Activation, LSTM
from keras.layers import Embedding
from keras.models import Sequential
from keras.preprocessing import sequence
from tensorflow import keras

import constant

with open('mehfi.csv', newline='', encoding='utf-8') as file:
    reader = csv.reader(file, delimiter=',')
    wine_dataset = [(entry[0], int(entry[1])) for entry in reader]

# beer_dataset = []
# wine_dataset = []
# for row in rows:
#     if int(row['wine/beer']) == 0:
#         wine_dataset += [(row['review'], int(row['type']))]
#     if int(row['wine/beer']) == 1:
#         beer_dataset += [(row['review'], int(row['type']))]


def create_model(dataset, file_name):
    dataset_size = len(dataset)
    output_dimension = max(x[1] for x in dataset)
    train, test = dataset[:dataset_size // 2], dataset[dataset_size // 2:]

    x_train, y_train = np.array([literal_eval(x[0]) for x in train]), np.array(
        [[int(y == x[1]) for y in range(output_dimension)] for x in train]).astype(int)
    x_test, y_test = np.array([literal_eval(x[0]) for x in test]), np.array(
        [[int(y == x[1]) for y in range(output_dimension)] for x in test]).astype(int)

    # set parameters:
    max_features = constant.WORDS_NUMBER
    maxlen = 400
    batch_size = 50
    embedding_dims = 128
    filters = 250
    kernel_size = 3
    hidden_dims = 250
    epochs = 12

    # print(x_train[0])
    # print(y_train[0])

    print(x_train)
    print(y_train)
    print(len(x_train), 'train sequences')
    print(len(x_test), 'test sequences')

    x_train = sequence.pad_sequences(x_train, maxlen=maxlen)
    x_test = sequence.pad_sequences(x_test, maxlen=maxlen)
    #

    model = Sequential()

    model.add(Embedding(max_features,
                        embedding_dims,
                        input_length=maxlen))
    model.add(LSTM(embedding_dims, dropout=0.2, recurrent_dropout=0.2))
    # model.add(Dropout(0.2))

    # #
    # model.add(Conv1D(filters,
    #                  kernel_size,
    #                  padding='valid',
    #                  activation='relu',
    #                  strides=1))
    # model.add(GlobalMaxPooling1D())
    # #

    # model.add(Dense(hidden_dims))
    # model.add(Dropout(0.2))
    # model.add(Activation('relu'))
    #
    model.add(Dense(output_dimension))
    model.add(Activation('sigmoid'))
    #
    model.compile(loss='binary_crossentropy',
                  optimizer='adam',
                  metrics=['categorical_accuracy'])
    model.fit(x_train, y_train,
              batch_size=batch_size,
              epochs=epochs)
    # print((y_test.shape))
    # print((y_test[0:50]))
    # model = keras.models.load_model('wine_type_model.h5')
    res = model.evaluate(x_test, y_test)
    print(res)

    model.save('lstm_wines.h5')


create_model(wine_dataset, 'wine_type_model')

# create_model(beer_dataset, 'beer_type_model')