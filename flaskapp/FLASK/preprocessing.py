# -*- coding: utf-8 -*-
"""
Created on Tue Feb  1 18:18:51 2022

@author: 50340
"""

# basic base
import nltk
import string
# English Preprocessing Base
from nltk.stem import WordNetLemmatizer

# Run the following code while you run the whole programming
# nltk.download('stopwords')
# nltk.download('punkt')
# nltk.download('words')
# nltk.download('wordnet')

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

# Define English Pre-processing Function
def Preprocess_English_Sentence(sentence):
    stopwords = nltk.corpus.stopwords.words('english')
    Ewords = set(nltk.corpus.words.words())
    Englishlemmatizer = WordNetLemmatizer()
    
    sentence_w_punct = "".join([i.lower() for i in sentence if i not in string.punctuation + '”“'])

    sentence_w_num = ''.join(i for i in sentence_w_punct if not i.isdigit())

    tokenize_sentence = nltk.tokenize.word_tokenize(sentence_w_num)

    words_w_stopwords = [i for i in tokenize_sentence if i not in stopwords]

    words_lemmatize = (Englishlemmatizer.lemmatize(w) for w in words_w_stopwords)

    sentence_clean = ' '.join(w for w in words_lemmatize if w.lower() in Ewords or not w.isalpha())

    return sentence_clean