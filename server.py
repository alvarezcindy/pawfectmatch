"""Dog Matching."""

import os
import requests

from jinja2 import StrictUndefined
from sqlalchemy import func, desc
from flask import Flask, render_template, request, flash, redirect, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from pprint import pprint, pformat
from random import shuffle

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

    dogs = call_api()

    return render_template("index.html", 
                           traits=traits,
                           dogs=dogs)
                           # names=names,

@app.route('/call-api.json')
def call_api():

    breeds = request.args.getlist("search_dogs[]")

    if not breeds:
        breeds = [None]

    dogs = []

    for breed in breeds:
        payload = {'key': PETFINDER_KEY,
                    'animal': 'dog',
                    'breed': breed,
                    'location': '94702',
                    # 'offset': 16,
                    'count': 10,
                    'format': 'json'
                    }

        data = requests.get(PETFINDER_URL + 'pet.find', params=payload)
        data = data.json()

        if data['petfinder']['pets'] != {}:

            results = data['petfinder']['pets']['pet']

            for result in results: 
                try:
                    dogs.append({'name': result['name']['$t'],
                                 'photos': result['media']['photos']['photo'][2]['$t'],
                                 'desc': result['description']['$t'][:70]})
                except: 
                  continue

    shuffle(dogs)

    if request.args.getlist("search_dogs[]"):
        return jsonify(dogs)

    return dogs

@app.route('/dog-list.json', methods=['POST'])
def dog_traits():
    pos_trait1 = request.form.get("pos_trait1")
    pos_trait2 = request.form.get("pos_trait2")
    pos_trait3 = request.form.get("pos_trait3")
    pos_trait4 = request.form.get("pos_trait4")
    pos_trait5 = request.form.get("pos_trait5")

    pos_traits = (pos_trait1, pos_trait2, pos_trait3, pos_trait4, pos_trait5)

    dogs = (db.session.query(Breed.name, func.count(Breed.breed_id))
                      .join(Rating)
                      .join(Characteristic)
                      .filter(((Characteristic.name==pos_trait1) |
                               (Characteristic.name==pos_trait2) |
                               (Characteristic.name==pos_trait3) |
                               (Characteristic.name==pos_trait4) |
                               (Characteristic.name==pos_trait5)) &
                              ((Rating.score==5) |
                               (Rating.score==4)))
                      .group_by(Breed.name)
                      .order_by(desc(func.count(Breed.breed_id))))

    dogs = dogs[0:10]

    return jsonify(pos_traits, dogs)

if __name__ == "__main__":

    #have to set debut=True to use debugger tool below
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(host="0.0.0.0")