import argparse
import csv

import matplotlib.pyplot as plt
import numpy as np

parser = argparse.ArgumentParser()
parser.add_argument("--input", required=True)
parser.add_argument("--output", required=True)
args = parser.parse_args()

with open(args.input + '.csv', newline='', encoding='utf-8') as file:
    reader = csv.reader(file, delimiter=',')
    dataset = [(row[0], int(row[1])) for row in reader]


def sort_dataset(dataset):
    unique, counts = np.unique([entry[1] for entry in dataset], return_counts=True)
    sorted_entries = sorted(zip(unique, counts), key=lambda entry: entry[1])
    return [entry[0] for entry in sorted_entries], [entry[1] for entry in sorted_entries]


def save_histogram(filename, unique, counts):
    plt.clf()
    plt.bar(unique, counts, 1)
    plt.savefig(filename)


def create_histogram(filename, dataset):
    unique, counts = sort_dataset(dataset)
    save_histogram(filename, unique, counts)


# beer_dataset = []
# wine_dataset = []
# for row in rows:
#     if int(row['wine/beer']) == 0:
#         wine_dataset += [(row['review'], int(row['type']))]
#     if int(row['wine/beer']) == 1:
#         beer_dataset += [(row['review'], int(row['type']))]
#
# create_histogram('wines.png', wine_dataset)
# create_histogram('beers.png', beer_dataset)

create_histogram('charts/' + args.output + '.png', dataset)
