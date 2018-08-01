"""Models and database functions for DogMatch project"""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

##############################################################################
# Models

class Breed(db.Model):
    """Dog breeds for app."""
    __tablename__ = "breeds"

    breed_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(100))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<Breed breed_id={self.breed_id} name={self.name}>"

    
class Rating(db.Model):
    """Characteristic ratings by dog breed."""
    __tablename__ = "ratings"

    rating_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    breed_id = db.Column(db.Integer, db.ForeignKey('breeds.breed_id'))
    char_id = db.Column(db. Integer, db.ForeignKey('characteristics.char_id'))
    score = db.Column(db.Integer)

    breeds = db.relationship('Breed', backref='ratings')

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<Rating rating_id={self.rating_id} breed_id={self.breed_id} char_id={self.char_id} score={self.score}>"


class Characteristic(db.Model):
    """Characteristics and their descriptions."""
    __tablename__ = "characteristics"

    char_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.String(10000))

    ratings = db.relationship('Rating', backref='characteristics')

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<Characteristic char_id={self.char_id} name={self.name} description={self.description}>"

##############################################################################
# Helper functions

def connect_to_db(app):
    """Connect the database to Flask app."""

    # Configure to use PostgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///dogs'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ECHO'] = True
    db.app = app
    db.init_app(app)


if __name__ == "__main__":

    from server import app

    connect_to_db(app)
    print("Connected to DB.")
