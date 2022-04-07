# -*- coding: utf-8 -*-
"""
Created on Mon Mar 28 16:42:24 2022

@author: 50340
"""

import re
import pandas as pd
from collections import Counter
from matplotlib import pyplot as plt
from sklearn.cluster import KMeans,MiniBatchKMeans
from sklearn.feature_extraction.text import TfidfVectorizer
from preprocessing import Preprocess_list_of_French_Sentence, Preprocess_list_of_English_Sentence

def transform(dataset, n_features=1000):
    vectorizer = TfidfVectorizer(max_df=0.7, max_features=n_features, min_df=0.01,
                                 use_idf=True, smooth_idf=True, lowercase=False
                                 , analyzer='word')
    X = vectorizer.fit_transform(dataset)
    return X, vectorizer

def train(X, vectorizer, true_k=10, minibatch=False, showLable=False):
    if minibatch:
        km = MiniBatchKMeans(n_clusters=true_k, init='k-means++', n_init=1,
                             init_size=1000, batch_size=1000, verbose=False)
    else:
        km = KMeans(n_clusters=true_k, init='k-means++', max_iter=300, n_init=1,
                    verbose=False)
    km.fit(X)
    if showLable:
        print("Top terms per cluster:")
        order_centroids = km.cluster_centers_.argsort()[:, ::-1]
        terms = vectorizer.get_feature_names()
        print(vectorizer.get_stop_words())
        for i in range(true_k):
            print("Cluster %d:" % i, end='')
            for ind in order_centroids[i, :10]:
                print(' %s' % terms[ind], end='')
            print()
    result = list(km.predict(X)) 
    print('Cluster distribution:')
    print(dict([(i, result.count(i)) for i in result])) 
    return -km.score(X)

def k_determin():
    dataset = list_test
    print("%d documents" % len(dataset))
    X, vectorizer = transform(dataset, n_features=500)
    true_ks = []
    scores = []
    for i in range(3, 10, 1):
        score = train(X, vectorizer, true_k=i) / len(dataset)
        print(i, score)
        true_ks.append(i)
        scores.append(score)
    plt.figure(figsize=(8, 4))
    plt.plot(true_ks, scores, label="error", color="red", linewidth=1)
    plt.xlabel("n_features")
    plt.ylabel("error")
    plt.legend()
    plt.show()
    plt.savefig

def main(list_test):
    dataset = list_test
    X, vectorizer = transform(dataset, n_features=500)
    print(vectorizer.vocabulary_)
    score = train(X, vectorizer, true_k=5, showLable=True) / len(dataset)
    print(score)

with open('./train.csv', 'r', encoding='UTF-8') as f:
    lines = [re.sub('[^a-z]+', ' ', line.strip().lower()) for line in f]
print(type(lines))
french_text = pd.DataFrame(lines, columns =['text'])
french_preprocess_list = Preprocess_list_of_French_Sentence(french_text['text'])
preprocess_list_all = "".join(french_preprocess_list)
list_test = preprocess_list_all.split(' ')
count = Counter()
for word in list_test:
    count[word] += 1

#k_determin()
main(list_test)