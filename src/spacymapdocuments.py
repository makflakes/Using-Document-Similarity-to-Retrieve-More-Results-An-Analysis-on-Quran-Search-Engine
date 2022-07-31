import pickle

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
from spacy.lemmatizer import Lemmatizer


import time

import regex as re
import pickle

#Mapping to spaCy vector space for each of the three settings
def verses(new_df, nlp):
    all_verses = new_df["Translation"].tolist()
    dj_verses = all_verses.copy()
    disjoint_verses = [nlp(verse) for verse in dj_verses]
    return disjoint_verses

def n_explanations(new_df, nlp):
   all_explanations_unprep = new_df["Tafsir"].tolist()    
   disjoints_unprep = all_explanations_unprep.copy()
   disjoint_explanations_unprep = [nlp(expl) for expl in disjoints_unprep]
   return disjoint_explanations_unprep

def p_explanations(new_df, nlp):
   all_explanations_prep = new_df["Clean_Text"].tolist()
   all_explanations_prep = [' '.join(ele) for ele in all_explanations_prep]
   disjoints_prep = all_explanations_prep.copy()
   disjoint_explanations_prep = [nlp(expl) for expl in disjoints_prep]
   return disjoint_explanations_prep