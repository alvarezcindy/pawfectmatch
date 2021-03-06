"""Dog Matching."""

import os
import requests

from jinja2 import StrictUndefined
from sqlalchemy import func, desc
from flask import Flask, render_template, request, flash, redirect, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from pprint import pprint, pformat
from random import shuffle
import json

from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse

from model import connect_to_db, db, Breed, Rating, Characteristic

#initialize Flask app
app = Flask(__name__)

app.secret_key = "SEEECREEEET"

#Raise an error if there's an undefined variable in Jinja
app.jinja_env.undefined = StrictUndefined

PETFINDER_KEY = os.environ.get('PETFINDER_KEY')
PETFINDER_URL = 'http://api.petfinder.com/'

TWILIO_SID = os.environ.get('TWILIO_SID')
TWILIO_TOKEN = os.environ.get('TWILIO_TOKEN')
TWILIO_NUM_FROM = os.environ.get('TWILIO_NUM_FROM')
TWILIO_NUM_TO = os.environ.get('TWILIO_NUM_TO')

client = Client(TWILIO_SID, TWILIO_TOKEN)

@app.route('/')
def index():
    """Homepage."""
    if 'quiz' not in session:
        traits = db.session.query(Characteristic.name, Characteristic.description).all()

        dogs = call_api()

        return render_template("index.html", 
                               traits=traits,
                               dogs=dogs)

    results = session['quiz']

    traits = (db.session.query(Characteristic.name, Characteristic.description)
                        .filter(Characteristic.name.in_(results))
                        .order_by(Characteristic.name)
                        )

    breed_info, breeds = dog_traits()
    dogs = call_api(breeds)
    print(traits, dogs, breeds, breed_info)
    return render_template("index2.html", 
                           traits=traits,
                           dogs=dogs,
                           breed_info=breed_info)


@app.route('/call-api.json')
def call_api(breeds=None):
    if breeds == None:
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
                    'count': 12,
                    'format': 'json'
                    }

        data = requests.get(PETFINDER_URL + 'pet.find', params=payload)
        data = data.json()

        if data['petfinder']['pets'] != {}:

            results = data['petfinder']['pets']['pet']

            for result in results: 
                try:
                  photos = result['media']['photos']['photo'][2]['$t']
                except: 
                  continue

                try:
                  breed1 = result['breeds']['breed'][0].get('$t', ' ')
                  # breed2 = result['breeds']['breed'][1].get('$t', ' ')
                  # breed = breed1 + ' & ' + breed2
                except:
                  breed = result['breeds']['breed'].get('$t', ' ')

                name = result['name'].get('$t', ' ')
                sex = result['sex'].get('$t', ' ')
                email = result['contact']['email'].get('$t', ' ')
                phone = result['contact']['phone'].get('$t', ' ')
                city = result['contact']['city'].get('$t', ' ')
                zipcode = result['contact']['zip'].get('$t', ' ')

                dogs.append({'name': name,
                             'photos': photos,
                             'breed': breed,
                             'sex': sex,
                             'email': email,
                             'phone': phone,
                             'city': city,
                             'zipcode': zipcode})

                # dogs.append({'name': result['name']['$t'],
                #             'photos': result['media']['photos']['photo'][2]['$t'],
                #             'desc': result['description']['$t'][:70],
                #             'breed': result['breeds']['breed']['$t']})

    shuffle(dogs)

    if request.args.getlist("search_dogs[]"):
        return jsonify(dogs)

    return dogs

@app.route('/dog-list.json', methods=['POST'])
def dog_traits():

    if 'quiz' not in session:
        pos_trait1 = request.form.get("pos_trait1")
        pos_trait2 = request.form.get("pos_trait2")
        pos_trait3 = request.form.get("pos_trait3")
        pos_trait4 = request.form.get("pos_trait4")
        pos_trait5 = request.form.get("pos_trait5")

        pos_traits = (pos_trait1, pos_trait2, pos_trait3, pos_trait4, pos_trait5)

    else:
        pos_traits = session.get('quiz')
        pos_trait1, pos_trait2, pos_trait3, pos_trait4, pos_trait5 = session.get('quiz')

    breeds = (db.session.query(Breed.name, func.count(Breed.breed_id))
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

        
    breed_list = [breed[0] for breed in breeds[0:10]]    

    dogs = db.session.query(Breed.name, Breed.description, Breed.image).filter(Breed.name.in_(breed_list)).all()

    if 'quiz' not in session:
        session['quiz'] = pos_traits
        return jsonify(pos_traits, dogs)
    return (dogs, breed_list)

@app.route('/breeds')
def breed_list():
    breeds = (db.session.query(Breed.name, Breed.image, Breed.description)
                        .order_by(Breed.name))
    return render_template('breed_list.html', 
                            breeds=breeds)

@app.route('/traits')
def trait_list():
    traits = (db.session.query(Characteristic.name, Characteristic.description)
                            .order_by(Characteristic.name))
    return render_template('trait_list.html', 
                            traits=traits)

@app.route('/send-sms', methods=['POST'])
def send_sms():
  to_num = request.form.get("to_num")
  text = request.form.get("text")
  photo = request.form.get("photo")
  breed = request.form.get("breed")
  contact = request.form.get("contact")
  name = request.form.get("name")

  message = client.messages.create(
                     body=text,
                     media_url=photo,
                     from_=TWILIO_NUM_FROM,
                     to=TWILIO_NUM_TO) 

  instructions = "If you'd like to learn more about " + str(name) + ". Respond with 'info' for details"
  client.messages.create(
                     body=instructions,
                     from_=TWILIO_NUM_FROM,
                     to=TWILIO_NUM_TO) 
  
@app.route("/sms", methods=['GET', 'POST'])
def reply_sms():

    resp = MessagingResponse()

    body = request.values.get('Body', None)

    if body == 'contact':
      resp.message("Email: pawparent@gmail.com ; Phone:(510) 555-1212")
    else:
      resp.message("Sorry! that was an invalid message. Please reply with 'contact' if you'd like additional information")

    return str(resp)
  

if __name__ == "__main__":

    #have to set debut=True to use debugger tool below
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(host="0.0.0.0")