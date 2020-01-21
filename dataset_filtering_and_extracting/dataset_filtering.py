import csv
import glob

from langdetect import detect
from nltk.corpus import wordnet as wn

# line_count = 0
dataset_csv = 'beer_dataset.csv'
# english_reviews_only_file = 'english_reviews.csv'


def save_to_one_file():
    with open(dataset_csv,
              mode='w',
              newline='',
              encoding='utf-8') as output_file:
        writer = csv.writer(output_file, delimiter=';')
        for file_name in glob.glob('./beer_reviews_folder/beer_reviews*.csv'):
            with open(file_name, encoding='utf-8', errors='ignore') as input_file:
                csv_reader = csv.reader(input_file, delimiter=';')
                for row in csv_reader:
                    writer.writerow(row)


def filter_by_language(input_file_name, language, output_file_name):
    language_reviews_counter = 0
    row_counter = 0
    detection_error_counter = 0
    with open(input_file_name,
              mode='r',
              encoding='utf-8',
              errors='ignore') as input_file:
        csv_reader = csv.reader(input_file, delimiter=';')
        with open(output_file_name,
                  mode='w',
                  newline='',
                  encoding='utf-8') as output_file:
            writer = csv.writer(output_file, delimiter=';')
            for row in csv_reader:
                row_counter += 1
                if len(row) < 4:
                    print(row)
                else:
                    try:
                        if detect(row[4]) == language:
                            writer.writerow(row)
                            language_reviews_counter += 1
                    except:
                        detection_error_counter += 1
    print("English reviews number: " + str(language_reviews_counter))
    print("All reviews number: " + str(row_counter))
    print("Errors of language detection: " + str(detection_error_counter))


def proceed(csv_file):
    global line_count
    csv_reader = csv.reader(csv_file, delimiter=';')
    for row in csv_reader:
        if line_count == 0:
            print(f'Column names are {", ".join(row)}')
            line_count += 1
        else:
            line_count += 1
    print(f'Processed {line_count} lines.')


def count_number_of_lines():
    for file_name in glob.glob('english_reviews.csv'):
        with open(file_name, encoding='utf-8') as csv_file:
            proceed(csv_file)


# filter_by_language(dataset_csv, 'en', english_reviews_only_file)
def filter_by_verb_type(input_file_name):
    valid_rec_counter = 0
    with open(input_file_name, mode='r', encoding='utf-8', errors='ignore') as input_file:
        csv_reader = csv.reader(input_file, delimiter=';')
        for row in csv_reader:
            if len(row) < 4:
                print(row)
            else:
                words = str.split(row[4])
                adj_counter = 0
                for w in words:
                    for synset in wn.synsets(w):
                        if synset.pos() == 'a':
                            adj_counter += 1
                            break
                if adj_counter >= 10:
                    valid_rec_counter += 1
    print("Number of reviews with more than 15 adjectives:" + str(valid_rec_counter))


# filter_by_verb_type("english_reviews.csv")


def count_adj(sentence):
    words = str.split(sentence)
    adj_counter = 0
    for w in words:
        for synset in wn.synsets(w):
            if synset.pos() == 'a':
                adj_counter += 1
                break
    return adj_counter


def count(sentence, type):
    words = str.split(sentence)
    verb_counter = 0
    for w in words:
        for synset in wn.synsets(w):
            if synset.pos() == type:
                verb_counter += 1
                break
    return verb_counter
