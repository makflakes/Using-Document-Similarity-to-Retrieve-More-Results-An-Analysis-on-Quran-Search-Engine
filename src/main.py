from hashlib import new
import sys

import warnings
warnings.filterwarnings('ignore')
import math

import nltk
from nltk.corpus import stopwords
import pandas as pd
from nltk.tokenize import word_tokenize
import spacy
from spacy.tokenizer import Tokenizer
import numpy as np
from nltk.stem import PorterStemmer

import collections
from collections import Counter
import more_itertools
import itertools

import time

import regex as re

#File Imports
import invertedindex as ii
import ranksmodule
import booleanretrieval
import spacymapdocuments
import spacymapresults
import versesuggestion


#IMPORTANT VARIABLES TO TINKER
subset_size = 1137 #the amount of rows to be taken from the humongous dataset (0 - for full dataset)
samples_invindex = 7 #the amount of samples of the inverted index to display (0 - for full inverted index)
samples_postlist = 7 #the amount of samples of postings list to display (0 - for full posting list)
samples_intersect = 7 #the amount of text samples of intersection to display (0 - all intersected tweets)

nltk.download('punkt')
nltk.download('stopwords')
english_sw = stopwords.words('english')


dataset_path = sys.argv[1]
use_saves = sys.argv[2]
suggestion = sys.argv[3]

#print(use_saves)

#Loading InvertedIndex and Posting List

import pickle

use_loaded_inverted_index = '1'

if use_saves == '0':
    use_loaded_inverted_index = '0' #change this to 0 to run the invertedindex code and not make use of preconstructed inverted index

global postlist 

result=[]

tic = time.perf_counter()

invindex = {}
postlist=[]

#print(use_loaded_inverted_index)

if use_loaded_inverted_index == '1':
    print('Loading inverted index from file...')
    with open("../pickle/inverted_index", "rb") as fp:   # Unpickling
       invindex = pickle.load(fp)
    
    print('Loading postings list from file...')
    with open("../pickle/postlist", "rb") as fp:   # Unpickling
        postlist = pickle.load(fp)
        
    print('Loading relevant tokenwords from file...')
    with open("../pickle/tokenwords", "rb") as fp:   # Unpickling
        tokenwords = pickle.load(fp)
    
    print('Loading preprocessed dataset...')
    new_df = pd.read_pickle('../pickle/new_df')
    
else:
    invindex, postlist, new_df, tokenwords = ii.index('../data/Quran.csv') #postlist stores the posting list, invertedindex stores the complete inverted index.

'''
#Printing first n elements of each (samples_invindex variable under IMPORTANT VARIABLES) and showing how index matching is synchronous (hashmap between tokenwords and posting list is a success).
if (samples_invindex==0):
    print("Full inverted index:")
    print(invindex)
else:
    print("\n First %d elements of inverted index" %samples_invindex)
    n_items = more_itertools.take(samples_invindex, invindex.items())
    print(n_items)
        
if (samples_postlist == 0):
    print("Full postings list:")
    print(postlist)
else:
    print("\nFirst %d elements of posting list" %samples_postlist)
    print(postlist[:samples_postlist])
'''  
    
    
#result = query( "nation") #Returns complete postlist for a single term
#print(result)

#result = query( "sin", "forgive") #Returns intersection of postlist of both terms.


#Spell Correction
import spacy.cli
#spacy.cli.download("en_core_web_lg")
nlp = spacy.load("en_core_web_lg")

tokenizer = Tokenizer(nlp.vocab)
tokenizer = nlp.tokenizer
all_words = set(list((itertools.chain(*[[t.text for t in tokenizer(row.lower()) if t.is_alpha] for row in new_df[~new_df['Tafsir'].isna()]['Tafsir'].to_list()]))))

#Ranking TF-IDF Vectors

clean_texts = new_df['Clean_Text'].to_list()

docfreq = {}
no_of_docs = len(clean_texts)


for t in invindex:
    docfreq[t] = invindex[t][0]
    
no_of_words = len(docfreq)

tfidf_ = ranksmodule.tfidf_comp(clean_texts, docfreq, no_of_docs, no_of_words)

wordDict = sorted(docfreq.keys())
tfidfVector = []

if use_saves == '0':
    print('Building TF-IDF Vectors...')
    tfidfVector = [ranksmodule.computeTFIDFVector(text, wordDict, tfidf_) for text in clean_texts]
else:
    with open("../pickle/tfIDF", "rb") as fp:   # Unpickling
       tfidfVector = pickle.load(fp)

#Loading Documents for Similarity and Suggestions

disjoint_verses = []
disjoint_explanations_prep = []
disjoint_explanations_unprep = []
disjoint_docs = []

if use_saves == '1':
    print('Loading spacy nlp objects from pickle files, this can take a moment...')
    if suggestion == '1':
        with open("../pickle/disjoint_expl_prep", "rb") as fp:   # Unpickling
            disjoint_explanations_prep = pickle.load(fp)
    if suggestion == '2':
        with open("../pickle/disjoint_expl_unprep", "rb") as fp:   # Unpickling
            disjoint_explanations_unprep = pickle.load(fp)
    if suggestion == '3':
        with open("../pickle/disjoint_verses", "rb") as fp:   # Unpickling
            disjoint_verses = pickle.load(fp)
    
    print('Completed!')

else:
    if suggestion =='1':
        disjoint_explanations_prep = spacymapdocuments.p_explanations(new_df, nlp)
    if suggestion =='2':
        disjoint_explanations_unprep=spacymapdocuments.n_explanations(new_df, nlp)
    if suggestion =='3':
        disjoint_verses=spacymapdocuments.verses(new_df, nlp)
        

if suggestion == '1':
    disjoint_docs = disjoint_explanations_prep
if suggestion == '2':
    disjoint_docs = disjoint_explanations_unprep
if suggestion == '3':
    disjoint_docs = disjoint_verses

toc = time.perf_counter()
print(f"Completed in {toc - tic:0.4f} seconds")


#Main Query Code:

print('\n Welcome to the Quran Search Engine :\n')


while True:

    results = []
    suggestedverses = []


    query = input('\nEnter a query (or enter q to end): ')

    if query=='q':
        break

    
    results, suggestedverses = versesuggestion.setting(suggestion, query, disjoint_docs, invindex, new_df, tokenwords, postlist, tfidfVector, nlp, all_words)
    #print(results)
    
    if results:
        print('Results :')
        print("\n".join("Chapter {}, Verse {}".format(*tup) for tup in results))      
    
        print("\nYou might also be interested in the following verses: \n")
        print("\n".join("Chapter {}, Verse {}".format(*tup) for tup in suggestedverses)) 

    else:
        print('\nNo results found!\n')

print('Thank you for using our search engine!')


