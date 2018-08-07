"""Dog Matching."""

import os
import requests

from jinja2 import StrictUndefined
from flask import Flask, render_template, request, flash, redirect, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from pprint import pprint, pformat

from model import connect_to_db, db, Breed, Rating, Characteristic

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

@app.route('/dog-list.json', methods=['POST'])
def dog_traits():
    pos_trait1 = request.form.get("pos_trait1")
    pos_trait2 = request.form.get("pos_trait2")
    pos_trait3 = request.form.get("pos_trait3")
    # neg_trait1 = request.form.get("neg_trait1")
    # neg_trait2 = request.form.get("neg_trait2")
    # neg_trait3 = request.form.get("neg_trait3")

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

    payload = {'key': PETFINDER_KEY,
               'animal': 'dog',
               'breed': 'Chihuahua',
               'location': '94702',
               'count': 1,
               'format': 'json'
               }

    data = requests.get(PETFINDER_URL + 'pet.find', params=payload)
    data = data.json()

    photos = data['petfinder']['pets']['pet']['media']['photos']['photo']

    # for photo in photos:
    #     if photo['@size'] != 'x':
    #       del photo

    #     {% for photo in photos %}
    #     {% if photo['@size'] == 'x' %}
    #         {{ photo['$t'] }}
    #     {% endif %}
    # {% endfor %}

    # results = data['pets']

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

    results = {'traits': pos_traits,
               'dogs': dogs[0:20],
               'photos': photos}

    return render_template('dog_list.html', traits=pos_traits, photos=photos, dogs=dogs[0:20])
    # return jsonify(results)

if __name__ == "__main__":

    #have to set debut=True to use debugger tool below
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(host="0.0.0.0")