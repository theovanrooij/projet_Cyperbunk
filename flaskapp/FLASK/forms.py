from flask_wtf import Form
from wtforms import SelectField, SubmitField,StringField
from wtforms.validators import DataRequired

class genreForm(Form):
    genre_possible = [("All_genre","Tous les genres"),
    ("Romance","Romance"),
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


class forumForm(Form):
    forum_possible = [("booknode","Booknode"),
    ("cyberpunkforum","Cyberpunk Forum"),
    ("sffchronicles","SFFChronicles"),
    ("reddit","Reddit"),
    ("sffworld","SFFworld"),
    
    ("usenet","Usenet")
    # ("reddit4","Reddit 4"),
    ]
    input = SelectField(u'Forum à afficher : ', choices=forum_possible)
    submit = SubmitField('Go')