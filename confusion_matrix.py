import argparse
import csv
from ast import literal_eval

import keras.models
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sn
from keras.utils import np_utils
from sklearn.metrics import confusion_matrix

parser = argparse.ArgumentParser()
parser.add_argument("--image", required=True)
parser.add_argument("--dataset", required=True)
parser.add_argument("--model", required=True)
args = parser.parse_args()


def plot_array(y_test, y_pred):
    array = confusion_matrix(y_test, y_pred)
    df_cm = pd.DataFrame(array)
    sn.heatmap(df_cm, annot=False, fmt="d")
    plt.figure(figsize=(10, 7))
    plt.show()
    plt.savefig('charts/' + args.output)


with open(args.dataset, newline='', encoding='utf-8') as file:
    reader = csv.reader(file, delimiter=',')
    dataset = [(row[0], int(row[1])) for row in reader]

x_test = np.array([literal_eval(x[0]) for x in dataset])
y_test = np_utils.to_categorical(np.array([x[1] for x in dataset]))

model = keras.models.load_model(args.model)
y_pred = np.argmax(model.predict(x_test), axis=1)
plot_array(np.argmax(y_test, axis=1), y_pred)
