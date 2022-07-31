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



global clean_texts

def tfidf_comp(clean_texts, docfreq, no_of_docs, no_of_words, method=None):
    
    tfidf = {}
    #total_tokens = len(tokensfreq)

    for i in range(len(clean_texts)):
        text = clean_texts[i]
        total_tokens = len(text)
        occurences = Counter(text)
    
        for token in text:
           
            if (method==None or method == 'natural'):
                tf = occurences[token]/total_tokens
            elif method == 'log':
                tf = 1 + np.log(occurences[token]/total_tokens)
            df = docfreq[token]
            idf = np.log(len(clean_texts)/(df+1))
            tfidf[token] = tf*idf
        

    tfidf = collections.OrderedDict(sorted(tfidf.items()))
    return tfidf


def computeTFIDFVector(text, wordDict, tfidf):
    tfidfVector = [0.0] * len(wordDict)
    
    for i, word in enumerate(wordDict):
        if word in text:
            tfidfVector[i] = tfidf[word]
    return tfidfVector


def dot_product(vector_x, vector_y):
    dot = 0.0
    for e_x, e_y in zip(vector_x, vector_y):
        dot += e_x * e_y
    return dot

def magnitude(vector):
    mag = 0.0
    for index in vector:
        mag += math.pow(index, 2)
    return math.sqrt(mag)


def cosine_score(text1, new_df, tfidfVector, text2=None):
    index_t1 = new_df["Original_Text"].str.contains(text1).idxmax()
    
    if text2 == None:
        
        sim_docs=[]
        score=[]
        doc_cos_pair ={}
       
        for i in range(len(tfidfVector)):
            cosim = dot_product(tfidfVector[index_t1], tfidfVector[i])/ (magnitude(tfidfVector[index_t1]) * magnitude(tfidfVector[i]))
            #sim_docs.append(cosim)
            
            doc_cos_pair[i] = cosim
            
        for w in sorted(doc_cos_pair, key=doc_cos_pair.get, reverse=True):
            sim_docs.append(w)
            score.append(doc_cos_pair[w])
                
            
        return(sim_docs[1:], score[1:])
            
        
    else:    
        index_t2 = new_df["Original_Text"].str.contains(text2).idxmax()
        cosim = dot_product(tfidfVector[index_t1], tfidfVector[index_t2])/ (magnitude(tfidfVector[index_t1]) * magnitude(tfidfVector[index_t2]))
    
    return cosim

def ranking(docids, query_list, new_df, tfidfVector):
    
    relevantquery = ' '.join(query_list)
    #print(relevantquery)
    ranktuple = []
    
    for i in docids:
        score=0
        if relevantquery in (new_df['Original_Text'].iloc[i]):
            score+=1
        
        score+=cosine_score(relevantquery, new_df, tfidfVector, new_df['Original_Text'].iloc[i])
        ranktuple.append((i,score))
        
        
    rankedtuple = sorted(ranktuple, key=lambda x: x[1], reverse=True)
    rankedverses = [x[0] for x in rankedtuple]
    
    chapverses_list = []
    for docs in rankedverses:
        chap = new_df['Chapter'].iloc[docs]
        verse = new_df['Verse'].iloc[docs]
        chapverses_list.append((chap,verse))
        
    
    return rankedverses, chapverses_list