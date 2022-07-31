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

#QUERY FUNCTION which takes two terms, by default term2=None in case only one argument is passed
def query_ir(termlist, explanation, new_df, tokenwords, postlist):
    
    #If only one argument is passed.
    if len(termlist)==1:
        chapverlist = []
        doclist=[]
        term1 = termlist[0]
        #print("\nPostings List for '" + term1 + "' is as follows :")
        #print(postlist[tokenwords.index(term1)])
        if term1 in tokenwords:
            for i in postlist[tokenwords.index(term1)]:
                if explanation==1:
                    print("\nChapter : " + str(new_df['Chapter'].iloc[i]))
                    print("VerseNo. : " + str(new_df['Verse'].iloc[i]))
                    print("\nVerse : " + str(new_df['Translation'].iloc[i]))
                    print("\nTafsir :" + str(new_df['Tafsir'].iloc[i]))
                    print("--------------------------------------------------")
                    
                chapver = '0'+ str(new_df['Chapter'].iloc[i]) + str(new_df['Verse'].iloc[i])
                chapverlist.append(chapver)
                doclist.append(i)
                
            
            return (chapverlist,doclist) #returns the postlist result for the specific token as determined by tokenwords (our basic hashmap) index for that word.
        else:
            return (chapverlist, doclist)
    
    
        
    #in the case that there are 2 or more terms from the query
    else: 
        chapverlist=[]
        
        collectedpostlists = []
        
        for i in range (0, len(termlist)):
            
            if termlist[i] in tokenwords:
                collectedpostlists.append(postlist[tokenwords.index(termlist[i])])
            else:
                continue
            
                        
        
        if collectedpostlists:
            intersectlist=list(set.intersection(*[set(x) for x in collectedpostlists]))  #Our soon to be intersection of both postlists.
        else:
            return chapverlist
        
        
        #PostList Intersection Logic
        '''
        We first check if both the iterators represent the same term. If they do, they get added to the intersection list.
        If not, the iterator with the smaller value goes to its next posting. This continues till both lists are exhausted.
        '''
        
        #PostList Intersection Completed
        
        samples = new_df[['Chapter', 'Verse', 'Translation','Tafsir']].iloc[intersectlist]
        
            
        if (len(intersectlist)!=0):
            
            for i in range(0,len(intersectlist)):
                if explanation==1:
                    print("\nChapter : " + str(samples['Chapter'].iloc[i]))
                    print("VerseNo. : " + str(samples['Verse'].iloc[i]))
                    print("\nVerse :\n " + str(samples['Translation'].iloc[i]))
                    print("\nTafsir :\n" + str(samples['Tafsir'].iloc[i]))
                    print("--------------------------------------------------")
                
                chapver = '0'+ str(samples['Chapter'].iloc[i]) + str(samples['Verse'].iloc[i])
                chapverlist.append(chapver)
        
        return(chapverlist, intersectlist)