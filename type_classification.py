from __future__ import print_function

import csv
from ast import literal_eval

import numpy as np
from keras.layers import Conv1D, GlobalMaxPooling1D
from keras.layers import Dense, Dropout, Activation
from keras.layers import Embedding
from keras.models import Sequential
from keras.preprocessing import sequence
from tensorflow import keras
from ast import literal_eval
import argparse
from pathlib import Path
import os.path

import constant

MODELS_DIR = 'models'
Path(MODELS_DIR).mkdir(exist_ok=True)

parser = argparse.ArgumentParser(description='Train neural network for given dataset and save to file')
parser.add_argument('-d', '--dataset', help='Dataset file', required=True)
parser.add_argument('-m', '--model', help='Name of model to save to .h5 file', required=True)
args = parser.parse_args()

with open(args.dataset, newline='', encoding='utf-8') as file:
    reader = csv.reader(file, delimiter=',')
    # rows = [row for row in reader]
    dataset = [(entry[0], int(entry[1])) for entry in reader]

def dump_dataset(modelname, dataset, dataset_suffix):
    filename = modelname + '_' + dataset_suffix + '.csv'
    with open(os.path.join(MODELS_DIR, filename), 'w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerows(dataset)

# beer_dataset = []
# wine_dataset = []
# for row in rows:
#     if int(row['wine/beer']) == 0:
#         wine_dataset += [(row['review'], int(row['type']))]
#     if int(row['wine/beer']) == 1:
#         beer_dataset += [(row['review'], int(row['type']))]


def create_model(dataset, file_name):
    dataset_size = len(dataset)
    output_dimension = max(x[1] for x in dataset) + 1
    train, test = dataset[:dataset_size // 2], dataset[dataset_size // 2:]

    dump_dataset(args.model, train, 'train')
    dump_dataset(args.model, test, 'test')

    x_train, y_train = np.array([literal_eval(x[0]) for x in train]), np.array(
        [[int(y == x[1]) for y in range(output_dimension)] for x in train]).astype(int)
    x_test, y_test = np.array([literal_eval(x[0]) for x in test]), np.array(
        [[int(y == x[1]) for y in range(output_dimension)] for x in test]).astype(int)

    # set parameters:
    max_features = constant.WORDS_NUMBER
    maxlen = 400
    batch_size = 100
    embedding_dims = 50
    filters = 250
    kernel_size = 3
    hidden_dims = 250
    epochs = 20

    # print(x_train[0])
    # print(y_train[0])
    print(len(x_train), 'train sequences')
    print(len(x_test), 'test sequences')

    x_train = sequence.pad_sequences(x_train, maxlen=maxlen)
    x_test = sequence.pad_sequences(x_test, maxlen=maxlen)
    #

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
    model.add(Activation('softmax'))
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
    model.save(os.path.join(MODELS_DIR, args.model) + '.h5')


create_model(dataset, 'wine_type_model')

# create_model(beer_dataset, 'beer_type_model')
