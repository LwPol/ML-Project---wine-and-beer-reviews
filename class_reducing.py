import argparse
import csv
import random
from collections import Counter

parser = argparse.ArgumentParser()
parser.add_argument("--type", choices=["wine", "beer"], required=True)
parser.add_argument("--max", type=int, required=True)
parser.add_argument("--min", type=int, required=True)
args = parser.parse_args()

dataset = []

with open('final_dataset.csv', newline='', encoding='utf-8') as file:
    type = 0 if args.type == 'wine' else 1
    reader = csv.DictReader(file, delimiter=',')
    dataset = [(row['review'], int(row['type'])) for row in reader if int(row['wine/beer']) == type]

random.shuffle(dataset)


def filter(dataset):
    c = Counter()
    dataset_distribution = Counter(entry[1] for entry in dataset)
    for entry in dataset:
        if args.max > c.get(entry[1], 0) and dataset_distribution.get(entry[1]) >= args.min:
            c.update([entry[1]])
            yield entry


dataset_filtered = list(filter(dataset))

with open(args.type + str(args.min) + '-' + str(args.max) + '.csv', mode='w', newline='',
          encoding='utf-8') as output_file:
    writer = csv.writer(output_file)
    writer.writerows(dataset_filtered)
