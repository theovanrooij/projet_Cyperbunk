from flask import Flask, flash, send_from_directory,redirect, render_template, request, url_for
from graphsforums import Articles
import json
import plotly
import pandas as pd
import plotly_express as px
# Load model
import pickle

from forms import genreForm
from preprocessing import Preprocess_English_Sentence
from werkzeug.utils import secure_filename

 # # save the model to disk
# filename = 'lasso_final_interpret.sav'

# model = pickle.load(open(filename, 'rb'))

import joblib

# filename="lasso_final_interpret.pkl"
# model = joblib.load(filename)




import numpy as np
import json
from sklearn.linear_model import LogisticRegression

def logistic_regression_to_json(lrmodel, file=None):
    if file is not None:
        serialize = lambda x: json.dump(x, file)
    else:
        serialize = json.dumps
    data = {}
    data['init_params'] = lrmodel.get_params()
    data['model_params'] = mp = {}
    for p in ('coef_', 'intercept_','classes_', 'n_iter_'):
        mp[p] = getattr(lrmodel, p).tolist()
    return serialize(data)

def logistic_regression_from_json(jstring):
    data = json.loads(jstring)
    model = LogisticRegression(**data['init_params'])
    for name, p in data['model_params'].items():
        setattr(model, name, np.array(p))
    return model


with open("lasso.txt",'r') as f:
  model = logistic_regression_from_json(f.read())

with open("graph_coef.txt",'r') as f:
  graphJSON_genres = f.read()

# filename = 'graph_coeff.pkl'
# fig = joblib.load(filename)
# graphJSON_genres = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
# import pickle
# # save the model to disk
# filename = 'gradient_boosting.sav'
# model = pickle.load(open(filename, 'rb'))


from sklearn.feature_extraction.text import CountVectorizer
with open("vocab.txt", "r",encoding="utf-8")as f :
    vocab = f.read().split("\n")
    vectorizer = CountVectorizer(max_features=3000,vocabulary=vocab,stop_words="english",binary=True)




app = Flask(__name__)

Articles = Articles()


def getPredictionFromNumber(number):
    if number == 1 :
        return "Cyberpunk"
    else : 
        return "Not Cyberpunk"




#   ### Gestion des pages web

@app.route('/')
def accueil():
    
    return render_template('accueil.html')

@app.route('/etude-cyberpunk')
def etude_cyberpunk():
    return render_template('etude_cyberpunk.html', articles = Articles )

@app.route('/sous-genres')
def sous_genres():
    return render_template('sous_genres.html')

@app.route('/babelio')
def babelio():
    return render_template('babelio.html')

@app.route('/autres-genres')
def autres_genres():

    form = genreForm()

    genre = request.args.get('input')
    if genre == None :
        genre = "All_genre"

    return render_template('autres_genres.html',form=form,graphJSON_genres=graphJSON_genres,genre=genre)

    # return render_template('autres_genres.html')

@app.route('/upload')
def upload_file():
   return render_template('upload.html')


@app.route('/prediction', methods = ['GET', 'POST'])
def prediction():
    if request.method == 'POST':
        f = request.files['file']
        f.save(secure_filename(f.filename))

        with open(f.filename,encoding="utf-8") as f:
            file_content = f.read()
            process_content = Preprocess_English_Sentence(file_content)

        matrix = vectorizer.fit_transform([process_content])
        probas = model.predict_proba(matrix.todense())
        if probas[0][1] > .5 :
            prediction = "Cyberpunk"
            proba = probas[0][1]
        else : 
            prediction = "Not Cyberpunk"
            proba = probas[0][0]
        proba = round(proba*100,2)
        return render_template('prediction.html',prediction=prediction,proba=proba)


if __name__ == '__main__':
    app.run(debug=True) #pour que les changements se mettent à jour en théorie??
    
