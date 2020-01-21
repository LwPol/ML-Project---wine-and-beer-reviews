import csv
from itertools import takewhile
from collections import Counter
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

with open('final_dataset.csv', newline='', encoding='utf-8') as file:
    reader = csv.DictReader(file, delimiter=',')
    rows = [row for row in reader]

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


beer_dataset = []
wine_dataset = []
for row in rows:
    if int(row['wine/beer']) == 0:
        wine_dataset += [(row['review'], int(row['type']))]
    if int(row['wine/beer']) == 1:
        beer_dataset += [(row['review'], int(row['type']))]

create_histogram('wines.png', wine_dataset)
create_histogram('beers.png', beer_dataset)
