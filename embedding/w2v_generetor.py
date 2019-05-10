import pickle
from nltk.stem.lancaster import LancasterStemmer
import pandas as pd
import numpy as np
# from gensim.models import FastText
import gensim
from gensim.models import FastText, Word2Vec
import string
from nltk.corpus import stopwords



def read_file(input_path):
    f = open(input_path, "r", encoding="utf8")
    print("reading file")
    return f

def read_tv_show_pkl_and_save_to_txt():

    text = ""

    for season in range(2,7):
        tv_show_input_path = "../parsed/season{}.pkl".format(season)

        f = open(tv_show_input_path, "rb")
        scenes = pickle.load(f)

        for scene in scenes:
            for dialog in scene._script:
                text += " " + dialog[1]

    tv_out_path = "../data/tv_show_text_raw/seasons_2_to_7.txt"

    f = open(tv_out_path, "w", encoding="utf8")
    f.write(text)
    f.close()

def parse_text(file):
    parsed_data = file.read() \
        .replace('“', "") \
        .replace('”', "") \
        .replace('‘', "") \
        .replace('’', "") \
        .replace('\f', "") \
        .replace('\n', " ") \
        .replace('\t', " ") \
        .replace(',', " ") \
        .replace('?', "") \
        .replace('…', "") \
        .replace('—', "") \
        .replace("'", "") \
        .rstrip().split('.')

    parsed_data = [x.translate(str.maketrans('', '', string.punctuation)) for x in parsed_data]

    s = set(stopwords.words('english'))

    parsed_data = [x.lower().strip().rstrip().split(' ') for x in parsed_data]

    # parsed_data = [list(filter(lambda w: not w in s, sentence)) for sentence in parsed_data]
    parsed_data = [list(filter(None, sentence)) for sentence in parsed_data]


    print("done preproccesing")

    return parsed_data


def create_w2v_model(parsed_data):
    model = Word2Vec(size=80, window=6, min_count=10, alpha=0.03)  # instantiate
    model.build_vocab(sentences=parsed_data)
    print("done building vocab")

    model.train(sentences=parsed_data, total_examples=model.corpus_count, epochs=50)  # train
    print("done training")
    return model


def save_model(model, output_model_path):
    model.save(output_model_path)
    print("model saved")


if __name__ == '__main__':
    # input_path = "../data/book_raw/all books2.txt"
    input_path = "../data/tv_show_text_raw/seasons_2_to_7.txt"
    output_model_path = "../data/w2v_models/tv_show_v1_model"

    is_books = False

    # read_tv_show_pkl_and_save_to_txt()

    file = read_file(input_path)

    parsed_data = parse_text(file)

    model = create_w2v_model(parsed_data)

    save_model(model, output_model_path)


