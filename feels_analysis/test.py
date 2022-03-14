import numpy as np
import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
### vectorizer
tfidf_ngrams = TfidfVectorizer(
    ngram_range=(1, 2), analyzer="word", binary=False)
tfidf_ngrams.fit(X)
X_vec = tfidf_ngrams.transform(X)