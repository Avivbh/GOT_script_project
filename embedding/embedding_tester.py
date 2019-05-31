from pprint import pprint
from scipy import spatial

from gensim.models import FastText
import pandas as pd
import numpy as np
from gensim import utils
from gensim.utils import SaveLoad
# from MulticoreTSNE import MulticoreTSNE as TSNE

# from embedding.utils import get_char_list, get_adj_from_json

pass

def cosine_similarity(word1, word2):
    cosine_similarity = 1 - spatial.distance.cosine(word1, word2)
    return np.abs(cosine_similarity)


def test_words_similarity(books_model, tv_show_model):
    list_of_words = ['stark', 'dragon', 'jon', 'cersei', 'arya']

    words_triples_list = [['man', 'woman', 'king'],
                          ['sansa', 'stark', 'jaime'],  #lannister
                          ['jaime', 'cersei', 'jon'],  #'bran', 'ned', 'theon', 'rickon', 'rob'
                          ['jaime', 'cersei', 'arya'],  #sansa
                          ['tywin', 'tyrion', 'ned'],  #arya
                          ['valar', 'morghulis', 'valar'],  #dohaeris
                          ['catelyn', 'brienne', 'tyrion'],  #bronn
                          ['brienne', 'catelyn', 'bronn'],  #tyrion # NOT simetric relation!
                          ['valyrian', 'steel', 'dornish'],  #wine
                          ['he', 'eat', 'she'],  #fuck
                          ['baelish', 'littlefinger', 'daenerys'],  # dany
                          ['westeros', 'qyburn', 'winterfell'],  # luwin
                          ['westeros', 'pycelle', 'winterfell'],  # luwin
                          ['qyburn', 'westeros', 'luwin'],  # winterfell
                          ['pycelle', 'westeros', 'luwin'],  # winterfell
                          ['luwin', 'winterfell', 'qyburn'],  # westeros
                          ['luwin', 'winterfell', 'pycelle'],  # westeros
                          ['winterfell', 'luwin', 'westeros'],  # qyburn, pycelle
                          ['ghost', 'jon', 'nymeria'],  # arya
                          ['jon', 'ghost', 'arya'],  # nymeria
                          ['arya', 'nymeria', 'jon'],  # ghost
                          ['nymeria', 'arya', 'ghost'],  # jon
                          ['sansa', 'lady', 'jon'],  # lord
                          ['daenerys', 'khaleesi', 'cersei'],  # mlady
                          ['ned', 'robert', 'tywin'],  # joffrey
                          ['jon', 'fighting', 'tyrion'],  # joffrey
                          ['ned', 'fighting', 'tyrion'],  # joffrey
                          ['cloaks', 'gold', 'night'],  # #watch
                          ['cloaks', 'janos', 'crows'],  # #watch
                          ['crows', 'mormont', 'cloaks'],  # #watch
                          ['watch', 'mormont', 'cloaks'],  # #watch
                          ['mormont', 'crows', 'janos'],  # #watch
                          ['mormont', 'watch', 'janos'],  # #watch
                          ['cloaks', 'janos', 'crows'],  # #watch
                          ['cloaks', 'janos', 'watch'],  # #watch
                          ['crows', 'watch', 'gold'],  # #landing
                          ['crows', 'watch', 'cloak'],  # #landing
                          ['cloaks', 'landing', 'watch'],  # joffrey
                          ['robert', 'fighting', 'tyrion'],  # joffrey
                          ['petyr', 'catelyn', 'jorah'],  # dany
                          ['jon', 'north', 'cersei'],  # landing, kingdoms (AKA king's landing)
                          ['jon', 'north', 'daenerys'],  # westeros, meereen, yunkai
                          ['brienne', 'catelyn', 'hodor'],  # bran, rickon
                          ['mountain', 'hound', 'jon'],  # theon, arya



                          # tests of nicknames
                          ['imp', 'tyrion', 'littlefinger'],  #baelish, pyter
                          ['dwarf', 'tyrion', 'littlefinger'],  #baelish, pyter
                          ['baelish', 'littlefinger', 'tyrion'],  #imp, dwarf
                          ['tyrion', 'imp', 'baelish'],  #littlefinger
                          ['tyrion', 'dwarf', 'baelish'],  #littlefinger
                          ['daenerys', 'khaleesi', 'joffrey'],  #mlady
                          ['robert', 'ned', 'joffrey'],  #tywin
                          ['daenerys', 'jorah', 'catelyn'],  #petyr
                          ['jorah', 'daenerys', 'petyr'],  #catelyn



                          ['white', 'walker', 'black'],  #westeros, meereen, yunkai
                          ['stannis', 'baratheon', 'robb'],  #stark
                          ['mountain', 'hound', 'jon'],  #theon, arya
                          ['baelish', 'littlefinger', 'clegane'],  # hound
                          ['littlefinger', 'baelish', 'onion'],  # davos
                          ['petyr', 'littlefinger', 'sandor'],  # hound
                          ['petyr', 'littlefinger', 'clegane'],  # hound
                          ['gregor', 'mountain', 'sandor'],  # hound
                          ['clegane', 'hound', 'clegane'],  # mountain
                          ['clegane', 'hound', 'jon'],  # mountain
                          ['clegane', 'mountain', 'clegane'],  # hound
                          ['littlefinger', 'baelish', 'hound'],  # clegane
                          ['tyrion', 'imp', 'sandor'],  # clegane
                          ['tyrion', 'imp', 'clegane'],  # clegane
                          ['jon', 'king', 'davos'],  # ser
                          ['stannis', 'king', 'davos'],  # ser
                          ['davos', 'ser', 'jon'],  # king

                          # Bastard
                          ['gendry', 'robert', 'jon'],  # ned
                          ['robert', 'gendry', 'ned'],  # jon
                          ['gendry', 'baratheon', 'jon'],  # stark
                          ['baratheon', 'gendry', 'stark'],  # jon
                          ['ned', 'jon', 'robert'],  # gendry
                          ['jon', 'ned', 'gendry'],  # robert
                          ['jon', 'stark', 'gendry'],  # baratheon


                          ['gendry', 'bastard', 'jon'],
                          ['bastard', 'gendry', 'bastard'],
                          ['bastard', 'jon', 'bastard'],
                          ['bastard', 'ramsay', 'bastard'],
                          ['ramsay', 'bolton', 'gendry'],  # baratheon
                          ['ramsay', 'roose', 'gendry'], # baratheon(weak)
                          ['ramsay', 'roose', 'gendry'], # baratheon(weak)
                          ['ramsay', 'roose', 'jon'],  # ned
                          ['roose', 'ramsay', 'robert'],  # gendry
                          ['robert', 'gendry', 'roose'],  # gendry
                          ['gendry', 'robert', 'ramsay'],  # boltons(weak),
                          ['jon', 'ned', 'ramsay'],  # boltons(weak), roose(strong) - V
                          ['jon', 'ned', 'gendry'],  # robert

                            # Treatment to bastars

                          # """
                          # Due to its unique history and culture, bastards in Dorne are not looked down upon the way they are in the rest of the Seven Kingdoms.
                          # """
                          ['landing', 'bastard', 'dorne'],  # something bad
                          ['dorne', 'bastard', 'landing'],  # something good

                          ['winterfell', 'bastard', 'dorne'],  # something bad
                          ['dorne', 'bastard', 'winterfell'],  # something good

                          ['gendry', 'robert', 'ramsay'],  # boltons(weak), roose - V
                          ['robert', 'gendry', 'roose'],  # boltons(weak), ramsay - V

                          ['jon', 'ned', 'ramsay'],  # boltons(weak), roose(strong) - V
                          ['jon', 'ned', 'roose'],  # boltons(weak), ramsay(strong) - V

                          # ['khaleesi', 'daenerys', 'jon'],

                          ]

    for word in list_of_words:
        book_most_similar = books_model.wv.most_similar_cosmul(positive=word)
        tv_most_similar = tv_show_model.wv.most_similar_cosmul(positive=word)
        print("\nWord: {}. \n\tBooks most similar - {} \n\tTV show most similar - {}".format(
            word, [x[0] for x in book_most_similar][:3], [x[0] for x in tv_most_similar][:3]
        ))

    for words_triples in words_triples_list:
        book_most_similar = [x[0] for x in books_model.wv.most_similar_cosmul(positive=[words_triples[1], words_triples[2]],
                                               negative=[words_triples[0]])[:5]]
        tv_most_similar = [x[0] for x in tv_show_model.wv.most_similar_cosmul(positive=[words_triples[1], words_triples[2]],
                                                               negative=[words_triples[0]])[:5]]
        print("\n{} is to {} like {} is to: \n\tBooks - {} \n\tTV show - {}".format(
            words_triples[0], words_triples[1], words_triples[2], book_most_similar, tv_most_similar
        ))




def dim_reduction_per_model(model, name):
    words_embd_dict = {}
    vocab_dict = model.wv.vocab

    for word in vocab_dict:
        words_embd_dict[word] = model[word]

    words_embd_df = pd.DataFrame(words_embd_dict).T

    print("\n\nstarting TSNE on the {}".format(name))
    tsne = TSNE(n_jobs=4)
    Y = tsne.fit_transform(words_embd_df)
    two_dim_df = pd.DataFrame(Y, index=words_embd_df.index)
    two_dim_df['source'] = name
    two_dim_df['word'] = two_dim_df.index
    return two_dim_df


def dim_reduction(books_model, tv_show_model):
    books_df = dim_reduction_per_model(books_model, 'books')
    tv_show_df = dim_reduction_per_model(tv_show_model, 'tv show')

    two_dim_df = pd.concat([books_df, tv_show_df])

    two_dim_df.to_csv('../data/w2v_embeddings_dataframes/tsne_2_dims.csv')

    pass


def get_womanly_words(model, adjectives_list, woman_words_list):
    words_embd_dict = {}
    for word in woman_words_list:
        try:
            words_embd_dict[word] = model[word]
        except KeyError:
            pass

    words_embd_df = pd.DataFrame(words_embd_dict).T
    woman_embd = np.array(words_embd_df.mean(axis=0), dtype=np.float32)

    similarity_list = []
    for word in adjectives_list:
        try:
            if model.wv.vocab[word].count < 20:
                continue
            similarity_tuple = (word, cosine_similarity(model[word], woman_embd))
            similarity_list.append(similarity_tuple)
        except KeyError:
            pass
    similarity_list = sorted(similarity_list,key=lambda x: x[1])
    return similarity_list


def get_similart_words_embd(model, source_mame = "Books"):
    woman_words_list = ['she', 'daughter', 'hers', 'her', 'mother', 'woman', 'girl', 'herself', 'female', 'sister',
                        'daughters', 'mothers', 'women', 'girls',
                        'femen', 'sisters', 'aunt', 'aunts', 'niece', 'nieces']

    man_words_list = ['he', 'son', 'his', 'him', 'father', 'man', 'boy', 'himself', 'male', 'brother', 'sons',
                      'fathers', 'men', 'boys', 'males', 'brothers', 'uncle',
                      'uncles', 'nephew', 'nephews']

    adjectives_list = ['bitch', 'fucker','fucked', 'sexy', 'pretty', 'ugly', 'killer', 'fighter', 'strong', 'thankless', 'tactful', 'distrustful', 'quarrelsome', 'effeminate', 'fickle',
                       'talkative', 'dependable', 'resentful', 'sarcastic', 'unassuming', 'changeable', 'resourceful',
                       'persevering', 'forgiving', 'assertive', 'individualistic', 'vindictive', 'sophisticated',
                       'persevering', 'forgiving', 'assertive', 'individualistic', 'vindictive', 'sophisticated',
                       'deceitful', 'impulsive', 'sociable', 'methodical', 'idealistic', 'thrifty', 'outgoing',
                       'intolerant', 'autocratic', 'conceited', 'inventive', 'dreamy', 'appreciative', 'forgetful',
                       'forceful', 'submissive', 'pessimistic', 'versatile', 'adaptable', 'reflective', 'inhibited',
                       'outspoken', 'quitting', 'unselfish', 'immature', 'painstaking', 'leisurely', 'infantile', 'sly',
                       'praising', 'cynical', 'irresponsible', 'arrogant', 'obliging', 'unkind', 'wary', 'greedy',
                       'obnoxious', 'irritable', 'discreet', 'frivolous', 'cowardly', 'rebellious', 'adventurous',
                       'enterprising', 'unscrupulous', 'poised', 'moody', 'unfriendly', 'optimistic', 'disorderly',
                       'peaceable', 'considerate', 'humorous', 'worrying', 'preoccupied', 'trusting', 'mischievous',
                       'robust', 'superstitious', 'noisy', 'tolerant', 'realistic', 'masculine', 'witty', 'informal',
                       'prejudiced', 'reckless', 'jolly', 'courageous', 'meek', 'stubborn', 'aloof', 'sentimental',
                       'complaining', 'unaffected', 'cooperative', 'unstable', 'feminine', 'timid', 'retiring',
                       'relaxed', 'imaginative', 'shrewd', 'conscientious', 'industrious', 'hasty', 'commonplace',
                       'lazy', 'gloomy', 'thoughtful', 'dignified', 'wholesome', 'affectionate', 'aggressive',
                       'awkward', 'energetic', 'tough', 'shy', 'queer', 'careless', 'restless', 'cautious', 'polished',
                       'tense', 'suspicious', 'dissatisfied', 'ingenious', 'fearful', 'daring', 'persistent',
                       'demanding', 'impatient', 'contented', 'selfish', 'rude', 'spontaneous', 'conventional',
                       'cheerful', 'enthusiastic', 'modest', 'ambitious', 'alert', 'defensive', 'mature', 'coarse',
                       'charming', 'clever', 'shallow', 'deliberate', 'stern', 'emotional', 'rigid', 'mild', 'cruel',
                       'artistic', 'hurried', 'sympathetic', 'dull', 'civilized', 'loyal', 'withdrawn', 'confident',
                       'indifferent', 'conservative', 'foolish', 'moderate', 'handsome', 'helpful', 'gentle',
                       'dominant', 'hostile', 'generous', 'reliable', 'sincere', 'precise', 'calm', 'healthy',
                       'attractive', 'progressive', 'confused', 'rational', 'stable', 'bitter', 'sensitive',
                       'initiative', 'loud', 'thorough', 'logical', 'intelligent', 'steady', 'formal', 'complicated',
                       'cool', 'curious', 'reserved', 'silent', 'honest', 'quick', 'friendly', 'efficient', 'pleasant',
                       'severe', 'peculiar', 'quiet', 'weak', 'anxious', 'nervous', 'warm']

    # adjectives_list = list(set(adjectives_list + get_adj_from_json()))

    # ------------------
    # woman_words_list = ['arya']
    # woman_words_list = get_char_list(male=False)
    #
    # man_words_list = ['sansa']
    # man_words_list = get_char_list(male=True)
    # ------------------



    manly_words = [x[0] for x in get_womanly_words(model, adjectives_list, man_words_list)]
    womanly_words = [x[0] for x in get_womanly_words(model, adjectives_list, woman_words_list)]

    print("\n{}:".format(source_mame))
    print("\nManly adjectives: \n\t{}".format(
        ", ".join(manly_words[:8])
    ))
    print("\nWomanly adjectives: \n\t{}".format(
        ", ".join(womanly_words[:8])
    ))


    return manly_words, womanly_words


if __name__ == '__main__':
    books_model_path = "../data/w2v_models/book_v1_model"
    tv_show_model_path = "../data/w2v_models/tv_show_v1_model"

    books_model = SaveLoad.load(books_model_path)
    tv_show_model = SaveLoad.load(tv_show_model_path)

    test_words_similarity(books_model, tv_show_model)

    # dim_reduction(books_model, tv_show_model)

    books_manly_words, books_womanly_words = get_similart_words_embd(books_model, source_mame='Books')
    tv_manly_words, tv_womanly_words = get_similart_words_embd(tv_show_model, source_mame='TV Show')

    similarity_df = pd.DataFrame([books_manly_words, books_womanly_words, tv_manly_words, tv_womanly_words ]).T
    similarity_df.columns = ['books manly words', 'books womanly words', 'tv manly words', 'tv womanly words']
    similarity_df.to_csv('../data/similarity_tables/manly_and_womanly_words.csv')

    pass

