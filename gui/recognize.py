from keras.models import load_model
from keras.preprocessing.text import tokenizer_from_json
from keras.preprocessing import sequence
import joblib
import numpy as np

def read_file(filename):
    with open(filename, encoding='utf-8') as file:
        return file.read()


recognizer = load_model('beers_and_wines_recognizer.h5')
tokenizer = tokenizer_from_json(read_file('tokenizer.json'))
encoder = joblib.load('type_encoder')

def recognize(review):
    categorical_review = tokenizer.texts_to_sequences([review])
    network_input = sequence.pad_sequences(np.array(categorical_review), maxlen=400)
    prediction = recognizer.predict(network_input)
    class_index = np.where(prediction == np.amax(prediction))[1][0]
    class_count = prediction.shape[1]
    encoded_class = np.array([int(i == class_index) for i in range(class_count)]).reshape(1, class_count)
    return encoder.inverse_transform(encoded_class)[0, 0]