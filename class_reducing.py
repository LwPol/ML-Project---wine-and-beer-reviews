import argparse
import code
import csv
import random
from collections import Counter

parser = argparse.ArgumentParser()
parser.add_argument("--file")
parser.add_argument("--type", choices=["wine", "beer"])
parser.add_argument("--threshold", type=int)
args = parser.parse_args()

dataset = []

with open('final_dataset.csv', newline='', encoding='utf-8') as file:
    type = 0 if args.type == 'wine' else 1
    reader = csv.DictReader(file, delimiter=',')
    dataset = [(row['review'], int(row['type'])) for row in reader if int(row['wine/beer']) == type]

random.shuffle(dataset)

c = Counter()


def chuj(dataset):
    c = Counter()
    for entry in dataset:
        if c.get(entry[1], 0) < args.threshold:
            c.update([entry[1]])
            yield entry


dataset_filtered = list(chuj(dataset))

with open(args.file, mode='w', newline='', encoding='utf-8') as output_file:
    writer = csv.writer(output_file)
    writer.writerows(dataset_filtered)

code.interact(local=locals())
