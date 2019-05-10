import pandas as pd
import numpy as np
# from gensim.models import FastText
import gensim
from gensim.models import FastText, Word2Vec
import string

books_path = "../data/book_raw/all books2.txt"
# books_path = "C:\\Users\\Dvir\\Desktop\\Desktop Icons\\Master\\NLP\\GOT books\\v3 1.AGameOfThrones-GeorgeR.R.Martin.txt"

output_model_path = "../data/w2v_models/book_v1_model"


f = open(books_path, "r", encoding="utf8")
print("reading file")


lines = f.read()\
    .replace('“', "")\
    .replace('”', "")\
    .replace('‘', "")\
    .replace('’', "")\
    .replace('\f', "")\
    .replace('\n', " ")\
    .replace('\t', " ")\
    .replace(',', " ") \
    .replace('?', "")\
    .replace('…', "")\
    .replace('—', "")\
    .replace("'", "")\
    .rstrip().split('.')

lines = [x.translate(str.maketrans('', '', string.punctuation)) for x in lines]
lines = [x.lower().strip().rstrip().split(' ') for x in lines]


print("done preproccesing")
pass


model = Word2Vec(size=50, window=4, min_count=1)  # instantiate
model.build_vocab(sentences=lines)
print("done building vocab")

model.train(sentences=lines, total_examples=len(lines), epochs=10)  # train
print("done training")
model.save(output_model_path)
pass