"""Utility file to seed dog_breeds database from data in seed_data/"""

import datetime
from sqlalchemy import func


from model import Breed, Rating, Characteristic, connect_to_db, db
from server import app

def load_breeds():

def load_ratings():

def load_characteristics():


if __name__ == "__main__":
    connect_to_db(app)
    db.create_all()

    load_users()
    load_movies()
    load_ratings()
    set_val_user_id()