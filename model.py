"""Models and database functions for DogMatch project"""
from flask_sqlalchemy import flask_sqlalchemy

db = SQLAlchemy()

##############################################################################
# Models

class Breed(db.Model):
    """Dog breeds for DogMatch website."""
    __tablename__ = "breeds"

    

