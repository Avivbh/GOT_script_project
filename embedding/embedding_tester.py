from pprint import pprint

from gensim.models import FastText
import pandas as pd
import numpy as np
from gensim import utils
from gensim.utils import SaveLoad


model_path = "../data/w2v_models/book_v1_model"


model = SaveLoad.load(model_path)


pprint(model.similar_by_word("king"))

pprint(model.similar_by_word("queen"))

pprint(model.similar_by_word("dragons"))

pprint(model.similar_by_word("khaleesi"))

pprint(model.wv.most_similar(positive=['man', 'khaleesi'], negative=['woman']))


pprint(model.wv.most_similar(positive=['jaime', 'jon'], negative=['cersei']))

pass

