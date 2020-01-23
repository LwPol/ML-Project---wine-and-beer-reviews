import argparse
import csv

import matplotlib.pyplot as plt
import numpy as np

parser = argparse.ArgumentParser()
parser.add_argument("--prefix", required=True)
args = parser.parse_args()


def sort_dataset(dataset):
    unique, counts = np.unique([entry[1] for entry in dataset], return_counts=True)
    sorted_entries = sorted(zip(unique, counts), key=lambda entry: entry[1])
    return [entry[0] for entry in sorted_entries], [entry[1] for entry in sorted_entries]


def save_histogram(main_title, unique, counts):
    plt.clf()
    plt.bar(unique, counts, 1)
    plt.title(label=main_title)
    plt.savefig('charts/' + main_title)


def extract_data(filename):
    with open('models/' + filename + '.csv', newline='', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter=',')
        dataset = [(row[0], int(row[1])) for row in reader]
    unique, counts = sort_dataset(dataset)
    return unique, counts


def create_histogram(prefix, dataset_type):
    main_title = prefix + '_' + dataset_type
    unique, counts = extract_data(main_title)
    save_histogram(main_title, unique, counts)


create_histogram(args.prefix, 'test')
create_histogram(args.prefix, 'train')
