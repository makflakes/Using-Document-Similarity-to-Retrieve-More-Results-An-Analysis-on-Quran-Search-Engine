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

#IMPORTANT VARIABLES TO TINKER
subset_size = 1137 #the amount of rows to be taken from the humongous dataset (0 - for full dataset)

nltk.download('punkt')
nltk.download('stopwords')
english_sw = stopwords.words('english')



class PostList(list):

    def add_new_arrival(self, sublist):
        self.append(sublist)    #append tuple to self

    def message_count(self):
        return len(self)

def index(filename):
    
    print("Reading file...")
    
    global df
    global new_df
    
    df = pd.read_csv(filename)
    
    #print(df)
    
    if (subset_size == 0):
        new_df = df
    else:
        new_df = df[0:subset_size]
    print(new_df)
    
    #Preprocessing and adding new column "Clean_Texts" which will form our searchable tokens and "Original_Text", which will preserve our text in string form.
    print("Removing NEWLINE and TAB")
    new_df['Text'] = new_df['Tafsir'].str.replace(r'\d+','')
    new_df["Text"] = new_df['Tafsir'].str.replace('NEWLINE','')
    new_df["Text"] = new_df['Tafsir'].str.replace('TAB','')
    new_df["Text"] = new_df['Tafsir'].str.replace('_','')
    
    
    print("Removing Punctuations")
    new_df["Text"] = new_df['Text'].str.replace('[^\w\s]','')
    new_df["Text"] = new_df['Text'].str.replace('\n','')
    new_df['Text']= new_df['Text'].str.lower()
    
    print("Removing stopwords")
    new_df['Clean_Text'] = new_df['Text'].apply(lambda x: ' '.join([word for word in str(x).split() if word not in (english_sw)]))
    
    print("Tokenizing and creating new columns...")
    new_df['Original_Text']=new_df['Text']
    new_df['Text']=new_df['Text'].apply(word_tokenize)
    new_df['Clean_Text']=new_df['Clean_Text'].apply(word_tokenize)
    
    
    #Initialising global precedence to some important variables
    global counts
    global tokendict
    global tokendict1
    global tokenwords
    global postsizes
    
    tokenslist = new_df['Clean_Text'].to_list() #creating a list of list out of explanation tokens
    flatlist = list(np.concatenate(tokenslist)) #creating a 1D list to count all unique tokens
    counts = Counter(flatlist) #counting tokens
    
    tokendict = dict(counts) #creating a dictionary of key=token and value=occurences
    
    tokenwords = sorted(list(tokendict.keys())) #extracting only tokens from the dict and making a list of all token words in alphabetical order. This will also act as a hashmap to arrange a token to a specific id (index in this case).
    
    inv_dict={} #our soon to be inverted index

    postinglist=[[] for i in range(len(tokenwords))] #initialising an empty list of list which will be our posting list

    
    
    #Creating Posting List :
    '''
    The idea is to iterate over each row in the dataframe. We pick the tokens from the Clean_Text column
    and check the tokens of the original tweet to see if a token does exist.
    If it does exist, we make note of the index of the dataframe (document number) and see if the posting list already has a value
    for this document number at the position determined by tokenwords. The position determined by tokenwords will determine which of the lists
    of list corresponds to which token and will fill exactly that list whenever a token appears.
    '''
    
    for index, rows in new_df.iterrows():
    
        print('Creating Posting List : %d/100' %(round(index/1000)), end='\r')
    
        for item in new_df['Clean_Text'][index]:
        
            if item in new_df['Text'][index]:
                
                if index not in postinglist[tokenwords.index(item)]:
                    postinglist[tokenwords.index(item)].append(index)
                    
    #Posting List Created!
                    
    postsizes=[len(x) for x in postinglist] #Retrieves size of each of the lists for each token is posting list
    
    zip_iterator = zip(tokenwords, postsizes)


    tokendict1 = dict(zip_iterator) #Creates a dictionary with key = 'token' and value = 'size of posting list for that token'
        
    #NEW LINES
    postlist1 = PostList()
    postlist1.add_new_arrival(postinglist)
    
    #print(postlist1[0][2])
    print("Successfully created posting list!")
    
    
    #Creating Inverted Index
    '''
    The inverted index is now simply created as a dictionary with the following attributes:
    key = 'token' extracted from tokendict1(our zipped dict)
    value = a list of lists with the firstlist having one element equal to the 'size' of the posting list taken from postsizes and
            the second list having all the postings taken from postinglist.
    '''
    
    i=0
    for word in tokenwords:
        if word in tokendict:
            print('Building Inverted Index : %d/100' %(round((i/220540)*100)), end='\r')
            inv_dict[word]=[]
            # append the new number to the existing array at this slot
            inv_dict[word].append(tokendict1[word])
            #NEW LINE
            inv_dict[word].append(postlist1[0][tokenwords.index(word)])
        
            i=i+1
    
    print("Successfully Built Inverted Index")
                  
    return (inv_dict, postinglist, new_df, tokenwords)