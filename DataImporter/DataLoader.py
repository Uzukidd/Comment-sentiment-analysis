import os

import pandas as pd
import numpy as np
import pickle

pd.set_option('display.max_columns', None)

pd.set_option('max_colwidth',100)


def trainingCommentsImport(path) :

    data = pd.read_csv(path)

    data = data.drop('user', axis = 1)\
        .drop('Unnamed: 0', axis = 1)\
        .sort_values(by = ['votes', 'comment_time'] , ascending = False)\
        .reset_index(drop=  True)

    return data

def phraseSetImport(path) :

    phrase = [line.strip() for line in open(path, 'r', encoding='utf-8').readlines()]

    res = {}

    for word in phrase :

        res[word] = 0

    return res

def trainingMovieImport(path) :

    data = pd.read_csv(path)

    # data['type'] = pd.Series([i.replace("'", '').replace('[', '').replace(']', '').replace(' ', '').split(',') for i in data['types']])

    return data

def save_obj(obj, name):

    with open(name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(name):
    with open(name + '.pkl', 'rb') as f:
        return pickle.load(f)