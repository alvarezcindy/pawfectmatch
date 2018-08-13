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

    payload = {'key': PETFINDER_KEY,
               'animal': 'dog',
               # 'breed': 'Rottweiler',
               'location': '94702',
               'count': 12,
               'format': 'json'
               }

    data = requests.get(PETFINDER_URL + 'pet.find', params=payload)
    data = data.json()

    results = data['petfinder']['pets']['pet']

    names = []
    photos = []
    desc = []

    for result in results: 
        names.append(result['name']['$t'])

        try:
            photos.append(result['media']['photos']['photo'][2]['$t'])
            desc.append(result['description']['$t'][:70])
        except: 
            photos.append('static/img_placeholder.jpg')
            desc.append('No Description')

    return render_template("index.html", 
                           traits=traits,
                           names=names,
                           photos=photos,
                           desc=desc)

@app.route('/dog-list.json', methods=['POST'])
def dog_traits():
    pos_trait1 = request.form.get("pos_trait1")
    pos_trait2 = request.form.get("pos_trait2")
    pos_trait3 = request.form.get("pos_trait3")

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

#SQL!
# SELECT breeds.name, COUNT(*) AS nums
# FROM breeds 
# JOIN ratings ON breeds.breed_id = ratings.breed_id
# JOIN characteristics ON ratings.char_id = characteristics.char_id
# WHERE
# ((characteristics.name='Affectionate With Family' 
# OR characteristics.name='Easy To Train'
# OR characteristics.name='Adapts Well to Apartment Living')
# AND (ratings.score=5 OR ratings.score=4))
# GROUP BY breeds.name
# HAVING COUNT(*) > 1
# ORDER BY nums DESC;
# LIMIT 30;


    dogs = dogs[0:10]

    return jsonify(pos_traits, dogs)

if __name__ == "__main__":

    #have to set debut=True to use debugger tool below
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(host="0.0.0.0")