import pandas as pd 
import itertools
import numpy as np
import spacy
from spacy.tokenizer import Tokenizer


#Levenshtein Distance Calculation
def levenshtein(token1, token2):
    size_x = len(token1) + 1
    size_y = len(token2) + 1
    matrix = np.zeros ((size_x, size_y))
    for x in range(size_x):
        matrix [x, 0] = x
    for y in range(size_y):
        matrix [0, y] = y

    for x in range(1, size_x):
        for y in range(1, size_y):
            if token1[x-1] == token2[y-1]:
                matrix [x,y] = min(
                    matrix[x-1, y] + 1,
                    matrix[x-1, y-1],
                    matrix[x, y-1] + 1
                )
            else:
                matrix [x,y] = min(
                    matrix[x-1, y] + 1,
                    matrix[x-1, y-1] + 1,
                    matrix[x, y-1] + 1
                )
    # print (matrix)
    return (matrix[size_x - 1, size_y - 1])

#Using Levenshtein
def spell_recommendation(query_token, tokens):
    scores  = {}
    for t in tokens:
        lev_dist = levenshtein(t, query_token)
        if lev_dist <= 1:
            scores[t] = lev_dist
            print(scores)
    return [i[0] for i in sorted(scores.items(), key=lambda kv: (kv[1], kv[0]))]

#Dictionary for Linguistic Variation
variation_dict = {('aadam'):'adam',
                    ('eve', 'hava'):'hawa',
                    ('enoch', 'idrees', 'edris', 'idrissa'): 'idris',
                    ('noah', 'nooh'): 'nuh',
                    ('hud', 'hood') : 'hud',
                    ('saleh', 'shaleh', 'sawleh') : 'salih',
                    ('abraham', 'ibraheem', 'ebrahem', 'ebrahim'): 'ibrahim',
                    ('lot'): 'lut',
                    ('ishmael', 'ismaeel', 'ismayl'): 'ismail',
                    ('isaac', 'ishaaq') : 'ishaq',
                    ('jacob', 'yaqoob', 'jakob', 'jakov', 'yakoob', 'yakub') : 'yaqub',
                    ('joseph', 'yousuf', 'yousef', 'yosef', 'josef', 'yoseph', 'yusof') : 'yusuf',
                    ('job', 'ayub', 'ayoob', 'ayyoob'): 'ayyub',
                    ('jethro', 'suhaib', 'shoaib', 'suhayb', 'shuaib'): 'shu`ayb',
                    ('moses', 'musha', 'moosa') : 'musa',
                    ('pharoah', 'firaun', 'pharoh'):'firawn',
                    ('david', 'davud', 'dawid'): 'dawud',
                    ('sulaiman') : 'solomon',
                    ('elisha'): 'ilyas',
                    ('jonah'): 'yunus',
                    ('zachariah', 'zakkariya', 'zacharia', 'zakariah', 'zakkariah'): 'zakariyya',
                    ('john'): 'yahya',
                    ('eesa', 'jesus'): 'isa', 
                    ('bakka', 'bakkah', 'mecca', 'makka') : 'makkah',
                    ('mohammed', 'muhammed', 'mohammad', 'mohd'): 'muhammad'}

