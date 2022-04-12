# -*- coding: utf-8 -*-
"""
Created on Mon Apr 11 17:18:03 2022

@author: 50340
"""

import pandas as pd 
import nltk
import string
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import Birch

data = pd.read_csv('./train.csv')
x = data.text

stopwords = nltk.corpus.stopwords.words('english')
Ewords = set(nltk.corpus.words.words())
Englishlemmatizer = WordNetLemmatizer()

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

x_change = []

x_change = Preprocess_list_of_English_Sentence(x)

vectorizer = TfidfVectorizer(min_df=2, ngram_range=(1,2), strip_accents='unicode', norm='l2', token_pattern=r"(?u)\b\w+\b")
X = vectorizer.fit_transform(x_change)
num_clusters = 10
birch_cluster = Birch(n_clusters=num_clusters)
birch_result = birch_cluster.fit_predict(X)
print("Predicting result: ", birch_result)

data['code number'] = birch_result
pd.DataFrame(data).to_excel('cyber.xlsx', sheet_name='Sheet1', index=False, header=True)