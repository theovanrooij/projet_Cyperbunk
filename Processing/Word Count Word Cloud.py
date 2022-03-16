# -*- coding: utf-8 -*-
"""
Created on Tue Mar 15 00:34:33 2022

@author: 50340
"""

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
import wordcloud
import re
from collections import Counter
# English Preprocessing Base
from nltk.stem import WordNetLemmatizer
# French Preprocessing Base     MAKE SURE GIT AND PIP HAS BEEN INSTALLED 
# AND RUN pip install git+https://github.com/ClaudeCoulombe/FrenchLefffLemmatizer.git IN CMD
from french_lefff_lemmatizer.french_lefff_lemmatizer import FrenchLefffLemmatizer
import matplotlib.pyplot as plt

# Run the following code while you run the whole programming
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('words')
nltk.download('wordnet')

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
    
# word count (English)

# train_data = pd.read_csv('./train.csv')

# print(train_data.head())

# English Pre-processing Test Set
# preprocess_list_all = "".join(preprocess_list)
#     
# list_test = preprocess_list_all.split(' ')
# 
# count = Counter()
# for word in list_test:
#         count[word] += 1
# 
# counts_top100 = count.most_common(100)
# print (counts_top100)
# 
# 
# wc = wordcloud.WordCloud(
#     background_color = 'white', 
#     max_words=200,
#     max_font_size=100
# )
# 
# word Cloud (English)
# wc.generate_from_frequencies(count)
# plt.imshow(wc)
# plt.axis('off')

# word count (French)
with open('./text.txt', 'r', encoding='UTF-8') as f:
    lines = [re.sub('[^a-z]+', ' ', line.strip().lower()) for line in f]
print(type(lines))
french_text = pd.DataFrame(lines, columns =['text'])
french_preprocess_list = Preprocess_list_of_French_Sentence(french_text['text'])
preprocess_list_all = "".join(french_preprocess_list)
list_test = preprocess_list_all.split(' ')
count = Counter()
for word in list_test:
    count[word] += 1
 
counts_top100 = count.most_common(100)
print (counts_top100)

# word Cloud (French)
 
wc = wordcloud.WordCloud(
    background_color = 'white', 
    max_words=200,
    max_font_size=100
)

wc.generate_from_frequencies(count)
plt.imshow(wc)
plt.axis('off')