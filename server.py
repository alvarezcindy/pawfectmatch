"""Dog Matching."""

from jinja2 import StrictUndefined

from flask import Flask, render_template, request, flash, redirect, session
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, Breed, Rating, Characteristic

import os

#initialize Flask app
app = Flask(__name__)

app.secret_key = "SEEECREEEET"

#Raise an error if there's an undefined variable in Jinja
app.jinja_env.undefined = StrictUndefined

PETFINDER_KEY = os.environ.get('PETFINDER_KEY')
PETFINDER_URL = 'http://api.petfinder.com/'

@app.route('/')
def index():
    """Homepage."""

    traits = db.session.query(Characteristic.name).all()
    return render_template("homepage.html", traits=traits)

@app.route('/dog-list', methods=['POST'])
def dog_traits():
    pos_trait1 = request.form.get("pos_trait1")
    pos_trait2 = request.form.get("pos_trait2")
    pos_trait3 = request.form.get("pos_trait3")
    neg_trait1 = request.form.get("neg_trait1")
    neg_trait2 = request.form.get("neg_trait2")
    neg_trait3 = request.form.get("neg_trait3")

    pos_traits = (pos_trait1, pos_trait2, pos_trait3)

    dogs = (db.session.query(Breed.name)
                      .join(Rating)
                      .join(Characteristic)
                      .filter(((Characteristic.name==pos_trait1) |
                               (Characteristic.name==pos_trait2) |
                               (Characteristic.name==pos_trait3)) &
                              ((Rating.score==5) |
                               (Rating.score==4)))
                      .group_by(Breed.name))

    # #SQL!
    # SELECT breeds.name
    # FROM breeds 
    # JOIN ratings ON breeds.breed_id = ratings.breed_id
    # JOIN characteristics ON ratings.char_id = characteristics.char_id
    # WHERE
    # ((characteristics.name='Affectionate With Family' 
    # OR characteristics.name='Easy To Train')
    # AND (ratings.score=5 OR ratings.score=4))
    # OR
    # ((characteristics.name='Amount Of Shedding' 
    # OR characteristics.name='Tendency to Bark or Howl')
    # AND (ratings.score=1 OR ratings.score=2))
    # GROUP BY breeds.name
    # LIMIT 30;

    return render_template("dog_list.html", 
                           traits=pos_traits,
                           dogs=dogs[0:20])

if __name__ == "__main__":

    #have to set debut=True to use debugger tool below
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(host="0.0.0.0")