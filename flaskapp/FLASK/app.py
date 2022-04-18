from flask import Flask, flash, send_from_directory,redirect, render_template, request, url_for
from graphsforums import Articles
import json
import plotly
import pandas as pd
import plotly_express as px
# Load model
import pickle


 # # save the model to disk
filename = 'finalized_model.sav'
lr = pickle.load(open(filename, 'rb'))

lr_global = lr.explain_global(name="Logistic Regression")

df = pd.DataFrame({"Word":lr_global.data()["names"],"Score":lr_global.data()["scores"]},index=lr_global.data()["names"])

df["Abs_score"]=df["Score"].apply(abs)

df["Color"] = df["Score"].apply(lambda x : 1 if x > 0 else 0)

df = df.sort_values("Abs_score",ascending=True)


data = df[df["Score"]!=0]
fig = px.bar(data,  y='Word',x='Score', color="Color", orientation='h',
            color_continuous_scale='Bluered_r')
fig.update(layout_coloraxis_showscale=False)
fig.update_yaxes(range=[len(data)-60, len(data)])
fig.update_layout(title={"text":"Récapitulatif des mots significatif du cyberpunk (bleu) contre ceux s'en éloignant"})

graphJSON_genres = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)


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

@app.route('/autres-genres')
def autres_genres():

    return render_template('autres_genres.html',graphJSON_genres=graphJSON_genres)

    # return render_template('autres_genres.html')

if __name__ == '__main__':
    app.run(debug=True) #pour que les changements se mettent à jour en théorie??
    
