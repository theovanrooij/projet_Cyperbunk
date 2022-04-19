from flask_wtf import Form
from wtforms import SelectField, SubmitField,StringField
from wtforms.validators import DataRequired

class genreForm(Form):
    genre_possible = [("All_genre","Tous les genres"),
    ("Romance","Romance"),
    ("Thriller","Thriller"),
    ("Crime","Crime"),
    ("Space","Space"),
    ("Thriller","Thriller"),
    ("Vampire","Vampire"),
    ("Fantasy","Fantasy"),
    ("ScienceFantasy","ScienceFantasy"),
    ("Steampunk","Steampunk"),
    ("Horreur","Horreur"),
    ("Dystopie","Dystopie"),
    ("Humour","Humour")]
    input = SelectField(u'Genre à comparer : ', choices=genre_possible)
    submit = SubmitField('Go')
