import argparse
import csv
import random
from ast import literal_eval

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sn
from keras import Sequential
from keras.layers import Conv1D, Dropout, Embedding, GlobalMaxPooling1D, Activation, Dense
from keras.utils import np_utils
from keras_preprocessing import sequence
from sklearn.metrics import confusion_matrix

import constant

parser = argparse.ArgumentParser()
parser.add_argument("--output", required=True)
parser.add_argument("--dataset", required=True)
args = parser.parse_args()

maxlen = 400

with open(args.dataset + '.csv', newline='', encoding='utf-8') as file:
    reader = csv.DictReader(file, delimiter=',')
    dataset = [row for row in reader]


def create_model(dataset):
    dataset_size = len(dataset)
    output_dimension = max(x[1] for x in dataset) + 1
    random.shuffle(dataset)
    train, test = dataset[:dataset_size * 3 // 4], dataset[dataset_size * 3 // 4:]

    x_train = np.array([literal_eval(x[0]) for x in train])
    y_train = np_utils.to_categorical(np.array([x[1] for x in train]))
    x_test = np.array([literal_eval(x[0]) for x in test])
    y_test = np_utils.to_categorical(np.array([x[1] for x in test]))

    # set parameters:

    # print(x_train[0])
    # print(y_train[0])

    x_train = sequence.pad_sequences(x_train, maxlen=maxlen)
    x_test = sequence.pad_sequences(x_test, maxlen=maxlen)

    max_features = constant.WORDS_NUMBER
    batch_size = 100
    embedding_dims = 50
    filters = 250
    kernel_size = 3
    hidden_dims = 250
    epochs = 2
    model = Sequential()

    model.add(Embedding(max_features,
                        embedding_dims,
                        input_length=maxlen))
    model.add(Dropout(0.2))

    #
    model.add(Conv1D(filters,
                     kernel_size,
                     padding='valid',
                     activation='relu',
                     strides=1))
    model.add(GlobalMaxPooling1D())
    #

    model.add(Dense(hidden_dims))
    model.add(Dropout(0.2))
    model.add(Activation('relu'))
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

    y_pred = model.predict(x_test)
    plot_array(y_test, y_pred)
    return model


def plot_array(y_test, y_pred):
    array = confusion_matrix(y_test, y_pred)
    df_cm = pd.DataFrame(array)
    sn.heatmap(df_cm, annot=False, fmt="d")
    plt.figure(figsize=(10, 7))
    plt.show()
    plt.savefig('charts/' + args.output + '.png')


create_model(dataset)
