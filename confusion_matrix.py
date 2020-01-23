import argparse
import csv
from ast import literal_eval

import keras.models
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sn
from keras.utils import np_utils
from keras_preprocessing import sequence
from sklearn.metrics import confusion_matrix

parser = argparse.ArgumentParser()
parser.add_argument("--classes_num", type=int, required=True)
parser.add_argument("--prefix", required=True)
args = parser.parse_args()


def translate_matrix_to_bigger_empty(input_matrix):
    translated_matrix = np.zeros((args.classes_num, args.classes_num))
    translated_matrix[min(y_test):, min(y_test):] = input_matrix
    return translated_matrix


def plot_array(y_test, y_pred):
    conf_matrix = confusion_matrix(y_test, y_pred)

    translated_matrix = translate_matrix_to_bigger_empty(conf_matrix)

    df_cm = pd.DataFrame(translated_matrix)
    ax = plt.axes()
    ax.set_title(args.prefix)
    plot = sn.heatmap(df_cm, annot=False, fmt="d", ax=ax, cmap="PiYG")
    ax.set_xlim(min(y_test), args.classes_num)
    ax.set_ylim(args.classes_num, min(y_test))
    fig = plot.get_figure()
    fig.savefig('charts/' + args.prefix + '.png')


with open('models/' + args.prefix + '_test.csv', newline='', encoding='utf-8') as file:
    reader = csv.reader(file, delimiter=',')
    dataset = [(row[0], int(row[1])) for row in reader]

x_test = np.array([literal_eval(x[0]) for x in dataset])
y_test = np_utils.to_categorical(np.array([x[1] for x in dataset]), num_classes=args.classes_num)

maxlen = 400
x_test = sequence.pad_sequences(x_test, maxlen=maxlen)

model = keras.models.load_model('models/' + args.prefix + '.h5')
scores = model.evaluate(x_test, y_test)
with open('scores.csv', encoding='utf-8', mode='a', newline='') as file:
    writer = csv.writer(file, delimiter=',')
    writer.writerow([args.prefix, *scores])
    file.close()

prediction = model.predict(x_test)
y_pred = np.argmax(prediction, axis=1)
y_test = np.argmax(y_test, axis=1)
plot_array(y_test, y_pred)
