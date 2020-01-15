from __future__ import print_function

import csv
import itertools
import random

from keras.preprocessing.text import Tokenizer

import constant

with open('128wine_varieties.csv', newline='', encoding='utf-8') as file:
    reader = csv.DictReader(file, delimiter=',')
    rows = [row for row in reader]

dataset = [list(a) for a in
           zip((row['description'] for row in rows), itertools.repeat(0), (row['variety'] for row in rows))]

with open('beers_final.csv', newline='', encoding='utf-8') as file:
    reader = csv.DictReader(file, delimiter=';')
    rows = [row for row in reader]

dataset = dataset + [list(a) for a in
                     zip((row['review'] for row in rows), itertools.repeat(1), (row['style'] for row in rows))]

random.shuffle(dataset)

t = Tokenizer(num_words=constant.WORDS_NUMBER)
texts = [text[0] for text in dataset]
t.fit_on_texts(texts)

dataset_processed = [list(a) for a in
                     zip(t.texts_to_sequences(texts), (entry[1] for entry in dataset), (entry[2] for entry in dataset))]

with open('tokenized.csv', mode='w', newline='', encoding='utf-8') as output_file:
    writer = csv.writer(output_file, delimiter=',')
    writer.writerow(['text vectorized', 'wine/beer', 'type'])
    for row in dataset_processed:
        writer.writerow(row)
