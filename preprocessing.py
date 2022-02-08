# -*- coding: utf-8 -*-
"""
Created on Tue Feb  1 18:18:51 2022

@author: 50340
"""

# basic base
import numpy as np
import pandas as pd
import os
import nltk
import string
# English Preprocessing Base
from nltk.stem import WordNetLemmatizer
# French Preprocessing Base     MAKE SURE GIT AND PIP HAS BEEN INSTALLED 
# AND RUN pip install git+https://github.com/ClaudeCoulombe/FrenchLefffLemmatizer.git IN CMD
from french_lefff_lemmatizer.french_lefff_lemmatizer import FrenchLefffLemmatizer

# Run the following code while you run the whole programming
# nltk.download('stopwords')
# nltk.download('punkt')
# nltk.download('words')
# nltk.download('wordnet')

# English Pre-processing
stopwords = nltk.corpus.stopwords.words('english')
Ewords = set(nltk.corpus.words.words())
Englishlemmatizer = WordNetLemmatizer()

# Define English Pre-processing Function
def Preprocess_list_of_English_Sentence(listofSentence):
    preprocess_list = []
    for sentence in listofSentence :
        
        sentence_w_punct = "".join([i.lower() for i in sentence if i not in string.punctuation])
        
        sentence_w_num = ''.join(i for i in sentence_w_punct if not i.isdigit())
        
        tokenize_sentence = nltk.tokenize.word_tokenize(sentence_w_num)
        
        words_w_stopwords = [i for i in tokenize_sentence if i not in stopwords]
        
        words_lemmatize = (Englishlemmatizer.lemmatize(w) for w in words_w_stopwords)
        
        sentence_clean = ' '.join(w for w in words_lemmatize if w.lower() in Ewords or not w.isalpha())
        # rebuild the text
        preprocess_list.append(sentence_clean)

    return preprocess_list

# French Pre-processing
french_stopwords = nltk.corpus.stopwords.words('french')
Fwords = set(line.strip() for line in open('./dictionnaire.txt'))
Frenchlemmatizer = FrenchLefffLemmatizer()

# Define English Pre-processing Function
def Preprocess_list_of_French_Sentence(listofSentence):
    preprocess_list = []
    for sentence in listofSentence :
        
        sentence_w_punct = "".join([i.lower() for i in sentence if i not in string.punctuation])
        
        sentence_w_num = ''.join(i for i in sentence_w_punct if not i.isdigit())
        
        tokenize_sentence = nltk.tokenize.word_tokenize(sentence_w_num)
        
        words_w_stopwords = [i for i in tokenize_sentence if i not in french_stopwords]
        
        words_lemmatize = (Frenchlemmatizer.lemmatize(w) for w in words_w_stopwords)
        
        sentence_clean = ' '.join(w for w in words_lemmatize if w.lower() in Fwords or not w.isalpha())
        # rebuild the text
        preprocess_list.append(sentence_clean)

    return preprocess_list
    
train_data = pd.read_csv('./train.csv')

# print(train_data.head())

# English Pre-processing Test Set
preprocess_list = Preprocess_list_of_English_Sentence(train_data['text'])
print('Base sentence : '+train_data['text'][2])
print('Cleaned sentence : '+preprocess_list[2])

# French Pre-processing Test Set
lst = ['C\'est un test pour lemmatizer','plusieurs phrases pour un nettoyage','eh voilà la troisième !']
french_text = pd.DataFrame(lst, columns =['text'])
french_preprocess_list = Preprocess_list_of_French_Sentence(french_text['text'])
print('Base sentence : '+ lst[1])
print('Cleaned sentence : '+ french_preprocess_list[1])