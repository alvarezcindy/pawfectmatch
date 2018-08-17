"""Utility file to seed dog_breeds database from data in seed_data/"""

from model import Breed, Rating, Characteristic, connect_to_db, db
from server import app
from pprint import pprint

import json

def load_breeds():
    """Load dog breeds from json file into database"""
    json_string = open("seed_data/breeds.json").read()
    breeds_dict = json.loads(json_string)

    for dog in breeds_dict:
        name = dog['breed']
        desc = dog['info']
        clean_desc = ''

        for each in desc[0:25]:
            clean_desc += each

        new_breed = Breed(name=name,
                          description=clean_desc)

        # Add new dog breed to session
        db.session.add(new_breed)

    db.session.commit()


def load_ratings():
    """Load characteristic ratings from json file into database"""
    json_string = open("seed_data/breeds.json").read()
    breeds_dict = json.loads(json_string)

    for dog in breeds_dict:
        name = dog['breed']
        ratings = dog['char_scores']

        for rating in ratings: 
            if rating[1] != ' ':
                char_name = rating[0]
                score = rating[1]

                breed_id = db.session.query(Breed.breed_id).filter(Breed.name==name).first()
                char_id = db.session.query(Characteristic.char_id).filter(Characteristic.name==char_name).first()

                new_rating = Rating(breed_id=breed_id[0], 
                                    char_id=char_id[0], 
                                    score=score)
                db.session.add(new_rating)

    db.session.commit()

def load_characteristics():
    """Load characteristics and descriptions from json file into database"""
    json_string = open("seed_data/clean_chars.json").read()
    chars_dict = json.loads(json_string)

    for key, value in chars_dict.items():
        name = key
        description = value
        new_char = Characteristic(name=name,
                                  description=description)

        # Add new dog characteristic to session
        db.session.add(new_char)

    db.session.commit()

if __name__ == "__main__":
    connect_to_db(app)
    db.create_all()

    load_breeds()
    load_characteristics()
    load_ratings()