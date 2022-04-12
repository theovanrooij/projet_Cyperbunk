from flask import Flask, flash, send_from_directory,redirect, render_template, request, url_for
from graphsforums import Articles
import os

app = Flask(__name__)

Articles = Articles()


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
    return render_template('autres_genres.html')

if __name__ == '__main__':
    app.run(debug=True) #pour que les changements se mettent à jour en théorie??
    
