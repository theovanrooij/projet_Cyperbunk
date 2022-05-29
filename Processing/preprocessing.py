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
# French Preprocessing Base     MAKE SURE GIT AND PIP HAS BEEN INSTALLED 
# AND RUN pip install git+https://github.com/ClaudeCoulombe/FrenchLefffLemmatizer.git IN CMD
from french_lefff_lemmatizer.french_lefff_lemmatizer import FrenchLefffLemmatizer

# Run the following code while you run the whole programming
# nltk.download('stopwords')
# nltk.download('punkt')
# nltk.download('words')
# nltk.download('wordnet')

nltk.download('stopwords')
nltk.download('punkt')
nltk.download('words')
nltk.download('wordnet')

# English Pre-processing
stopwords = nltk.corpus.stopwords.words('english')
Ewords = set(nltk.corpus.words.words())
Englishlemmatizer = WordNetLemmatizer()

Fwords = set(line.strip() for line in open('../Processing/dictionnaire.txt',encoding="utf-8"))

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


# Define English Pre-processing Function
def Preprocess_list_of_French_Sentence(listofSentence):
    # French Pre-processing
    french_stopwords = nltk.corpus.stopwords.words('french')
    Fwords = set(line.strip() for line in open('./dictionnaire.txt'))
    Frenchlemmatizer = FrenchLefffLemmatizer()
    
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
    
# Define English Pre-processing Function
def Preprocess_French_Sentence(sentence):
    # French Pre-processing
    french_stopwords = nltk.corpus.stopwords.words('french')
    
    Frenchlemmatizer = FrenchLefffLemmatizer()
    
        
    sentence_w_punct = "".join([i.lower() for i in sentence if i not in string.punctuation])

    sentence_w_num = ''.join(i for i in sentence_w_punct if not i.isdigit())

    tokenize_sentence = nltk.tokenize.word_tokenize(sentence_w_num)

    words_w_stopwords = [i for i in tokenize_sentence if i not in french_stopwords]

    words_lemmatize = (Frenchlemmatizer.lemmatize(w) for w in words_w_stopwords)

    sentence_clean = ' '.join(w for w in words_lemmatize if w.lower() in Fwords or not w.isalpha())

    return sentence_clean
    