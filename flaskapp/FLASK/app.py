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
filename = 'finalized_model.sav'
model = pickle.load(open(filename, 'rb'))

model_global = model.explain_global(name="Logistic Regression")

df = pd.DataFrame({"Word":model_global.data()["names"],"Score":model_global.data()["scores"]},index=model_global.data()["names"])

df["Abs_score"]=df["Score"].apply(abs)

df["Color"] = df["Score"].apply(lambda x : 1 if x > 0 else 0)

df = df.sort_values("Abs_score",ascending=True)


data = df[df["Score"]!=0]
fig = px.bar(data,  y='Word',x='Score', color="Color", orientation='h',
            color_continuous_scale='Bluered_r')
fig.update(layout_coloraxis_showscale=False)
fig.update_yaxes(range=[len(data)-60, len(data)])
fig.update_layout(title={"text":"Récapitulatif des mots significatif du cyberpunk (bleu) contre ceux s'en éloignant"})



# import shap
# filename = 'gradient_boosting.sav'
# model = pickle.load(open(filename, 'rb'))


# explainer = shap.TreeExplainer(model)
# shap_values = explainer.shap_values(X_test_bag_resample)

# mean_shap = shap_values.mean(axis=0)
# res = {vocab[i]: mean_shap[i] for i in range(len(vocab))}

# df_shap = pd.DataFrame.from_dict(res,orient="index").reset_index().rename(columns={0:"Score"})

# df_shap["Abs_score"]=df_shap["Score"].apply(abs)

# df_shap["Color"] = df_shap["Score"].apply(lambda x : 1 if x > 0 else 0)

# df_shap = df_shap.sort_values("Abs_score",ascending=True)

# from IPython.display import HTML
# import plotly.express as px
# data = df_shap[df_shap["Score"]!=0]
# fig_tree = px.bar(data,  y='index',x='Score', color="Color", orientation='h',
#             color_continuous_scale='Bluered_r')
# fig_tree.update(layout_coloraxis_showscale=False)
# fig.update_yaxes(range=[len(data)-60, len(data)])
# fig_tree.update_layout(title={"text":"Récapitulatif des mots significatif du cyberpunk (touge) contre ceux s'en éloignant"})


from sklearn.feature_extraction.text import CountVectorizer
with open("vocab.txt", "r",encoding="utf-8")as f :
    vocab = f.read().split("\n")
    vectorizer = CountVectorizer(max_features=3000,vocabulary=vocab,stop_words="english",binary=True)


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
    
