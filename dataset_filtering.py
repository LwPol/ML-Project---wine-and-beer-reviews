import csv
import glob

from langdetect import detect

line_count = 0
dataset_csv = 'beer_dataset.csv'
english_reviews_only_file = 'english_reviews.csv'


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
    for file_name in glob.glob('./beer_reviews_folder/beer_reviews*.csv'):
        with open(file_name, encoding='utf-8', errors='ignore') as csv_file:
            proceed(csv_file)


filter_by_language(dataset_csv, 'en', english_reviews_only_file)
