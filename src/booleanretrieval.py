import sys

import warnings
warnings.filterwarnings('ignore')
import math

import nltk
from nltk.corpus import stopwords
import pandas as pd
from nltk.tokenize import word_tokenize
import numpy as np
from nltk.stem import PorterStemmer

import collections
from collections import Counter
import more_itertools

import time

import regex as re
import pickle

import ranksmodule
import querycorrection
import queryanswering

def boolean_retrieval(query, invindex, new_df, tokenwords, postlist, tfidfVector, all_words, explanation=0):
    print("Query :", query)
    
    query=query.lower()
    tokens = re.findall(r'([A-Za-z]+)',query)

    accepted_pos = ['VBN','VBG','VB','RP','RBS','RBR','RB','NNS','NNP','NN','JJS','JJR','JJ']

    query_words = nltk.pos_tag(tokens)

    query_list =[]

    for i in range(0,len(query_words)):
        if (query_words[i][1] in accepted_pos) and (query_words[i][0]!='story') and (query_words[i][0]!='be') and (query_words[i][0]!='i') :
            query_list.append(query_words[i][0])
    
    
    for i in range(len(query_list)):
        if query_list[i] not in invindex.keys():   
            for key, value in querycorrection.variation_dict.items():
                if query_list[i] in key:
                    query_list[i] = querycorrection.variation_dict[key]
            
            corrected_token = querycorrection.spell_recommendation(query_list[i], all_words)

            if corrected_token:
                query_list[i]=corrected_token[0]

    print('Showing results for relevant words :', query_list)

    chapvers,doclist = queryanswering.query_ir(query_list, explanation, new_df, tokenwords, postlist)


    
    #print(query_list)
    
    ranks = ranksmodule.ranking(doclist, query_list, new_df, tfidfVector)
    
    return query_list, chapvers, doclist