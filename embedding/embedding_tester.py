from pprint import pprint

from gensim.models import FastText
import pandas as pd
import numpy as np
from gensim import utils
from gensim.utils import SaveLoad


books_model_path = "../data/w2v_models/book_v1_model"
tv_show_model_path = "../data/w2v_models/tv_show_v1_model"


books_model = SaveLoad.load(books_model_path)
tv_show_model = SaveLoad.load(tv_show_model_path)



list_of_words = ['dragon', 'jon', 'cersei', 'arya']

words_triples_list = [['man','woman','king'],
                      ['jaime', 'cersei', 'jon'],
                      ['jaime', 'cersei', 'arya']
                      ]



for word in list_of_words:
    book_most_similar = books_model.wv.most_similar_cosmul(positive=word)[0][0]
    tv_most_similar = tv_show_model.wv.most_similar_cosmul(positive=word)[0][0]
    print("\nWord: {}. \n\tBooks most similar - {} \n\tTV show most similar - {}".format(
        word, book_most_similar, tv_most_similar
    ))

for words_triples in words_triples_list:
    book_most_similar = books_model.wv.most_similar_cosmul(positive=[words_triples[1], words_triples[2]], negative=[words_triples[0]])[0][0]
    tv_most_similar = tv_show_model.wv.most_similar_cosmul(positive=[words_triples[1], words_triples[2]], negative=[words_triples[0]])[0][0]
    print("\n{} is to {} like {} is to: \n\tBooks - {} \n\tTV show - {}".format(
        words_triples[0],words_triples[1],words_triples[2], book_most_similar, tv_most_similar
    ))

pass


