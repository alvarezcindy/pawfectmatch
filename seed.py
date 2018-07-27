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
        new_breed = Breed(name=name)

        # Add new dog breed to session
        db.session.add(new_breed)
        
    db.session.commit()


# def load_ratings():
#     """Load characteristic ratings from json file into database"""

# def load_characteristics():
#     """Load characteristics and descriptions from json file into database"""


if __name__ == "__main__":
    connect_to_db(app)
    db.create_all()

    load_breeds()