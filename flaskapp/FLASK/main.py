from flask import Flask, flash, send_from_directory,redirect, render_template, request, url_for
from graphsforums import Articles
import json

from forms import genreForm,forumForm
from preprocessing import Preprocess_English_Sentence
from werkzeug.utils import secure_filename
import os

import numpy as np
from sklearn.linear_model import LogisticRegression

import plotly
import plotly_express as px
import pandas as pd

from sklearn.feature_extraction.text import CountVectorizer


from interpret.glassbox import LogisticRegression as LR_interpret



def logistic_regression_from_json(jstring):
    data = json.loads(jstring)
    model = LogisticRegression(**data['init_params'])
    for name, p in data['model_params'].items():
        setattr(model, name, np.array(p))
    return model

def init_model() :
    with open("vocab.txt", "r",encoding="utf-8")as f :
        vocab = f.read().split("\n")
        vectorizer = CountVectorizer(max_features=3000,vocabulary=vocab,stop_words="english",binary=True)

    #Chargement du modèle
    with open("lasso.txt",'r') as f:
        lr = logistic_regression_from_json(f.read())

    model = LR_interpret()
    model.sk_model_ = lr
    model.feature_names = vocab
    return model,vectorizer

def load_explain_graph():
    #Chargement du graph
    with open("graph_coef.txt",'r') as f:
        return f.read()







app = Flask(__name__)

Articles = Articles()


def getPredictionFromNumber(number):
    if number == 1 :
        return "Cyberpunk"
    else : 
        return "Not Cyberpunk"

def getFigurePredict(model_local):
    df = pd.DataFrame({"Word":model_local.data(0)["names"],"Score":model_local.data(0)["scores"]},index=model_local.data(0)["names"])
    fig = None
    df["Abs_score"]=df["Score"].apply(abs)

    df["Color"] = df["Score"].apply(lambda x : 1 if x > 0 else 0)

    df = df.sort_values("Abs_score",ascending=True)
    
    data = df[df["Score"]!=0]
    fig = px.bar(data,  y='Word',x='Score', color="Color", orientation='h',color_continuous_scale='Bluered_r')
    fig.update(layout_coloraxis_showscale=False)
    
    fig.update_xaxes(range=[-2.7, 2.99])
    fig.update_yaxes(range=[len(data)-60, len(data)])
    fig.update_layout(title={"text":"Récapitulatif des mots présent dans le texte pesant pour le cyberpunk (bleu) contre ceux contre"})
    return fig


#   ### Gestion des pages web

@app.route('/')
def accueil():
    
    return render_template('accueil.html')

@app.route('/etude-cyberpunk')
def etude_cyberpunk():
    form = forumForm()

    forum = request.args.get('input')
    if forum == None :
        forum = "booknode"
    forumDict={
        "booknode":"Booknode",
    "sffworld":"SFFworld",
    "cyberpunkforum":"Cyberpunk Forum",
    "usenet":"Usenet",
    "sffchronicles":"SFFChronicles",
    "reddit":"Reddit",
    }
    forumName = forumDict[forum]
    return render_template('etude_cyberpunk.html', articles = Articles,form=form,forum=forum,forumName=forumName )

@app.route('/sous-genres')
def sous_genres():
    return render_template('sous_genres.html')

@app.route('/babelio')
def babelio():
    return render_template('babelio.html')

@app.route('/autres-genres', methods= ['GET'])
def autres_genres():
    global graphJSON_genres

    form = genreForm()

    error  = request.args.get('extension')

    genre = request.args.get('input')
    
    if genre == None :
        genre = "All_genre"

    return render_template('autres_genres.html',form=form,graphJSON_genres=graphJSON_genres,genre=genre,error=error)

    # return render_template('autres_genres.html')

@app.route('/upload')
def upload_file():
   return render_template('upload.html')


@app.route('/prediction', methods = ['GET', 'POST'])
def prediction():
    global model
    if request.method == 'POST':
        f = request.files['file']
        filename = secure_filename(f.filename)
        if filename.split(".")[1] != "txt":
            return redirect("/autres-genres?extension=wrong", code=302)
        else :
            f.save(filename)

        with open(filename,encoding="utf-8") as fp:
            file_content = fp.read()
        process_content = Preprocess_English_Sentence(file_content)

       

        matrix = vectorizer.fit_transform([process_content])


        model_local = model.explain_local(pd.DataFrame(matrix.todense()), name="Logistic Regression")
        proba = model_local.data(0)["perf"]["predicted_score"]
        proba = round(proba*100,2)
        prediction = getPredictionFromNumber(model_local.data(0)["perf"]["predicted"])

        fig = getFigurePredict(model_local)

        Graph_predict= json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        os.remove(filename)
        return render_template('prediction.html',prediction=prediction,proba=proba, Graph_predict=Graph_predict)

model,vectorizer = init_model()
graphJSON_genres = load_explain_graph()
if __name__ == '__main__':
    
    app.run(debug=True) #pour que les changements se mettent à jour en théorie??
    
