"""Dog Matching."""

from jinja2 import StrictUndefined

from flask import Flask, render_template, request, flash, redirect, session
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, Breed, Rating, Characteristic

#initialize Flask app
app = Flask(__name__)

app.secret_key = "SEEECREEEET"

#Raise an error if there's an undefined variable in Jinja
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""

    traits = db.session.query(Characteristic.name).all()
    return render_template("homepage.html", traits=traits)

@app.route('/dog-breeds', methods=['POST'])
def dog_traits():
    pos_trait1 = request.form.get("pos_trait1")
    pos_trait2 = request.form.get("pos_trait2")
    pos_trait3 = request.form.get("pos_trait3")
    neg_trait1 = request.form.get("neg_trait1")
    neg_trait2 = request.form.get("neg_trait2")
    neg_trait3 = request.form.get("neg_trait3")

    pos_traits = (pos_trait1, pos_trait2, pos_trait3)
    neg_traits = (neg_trait1, neg_trait2, neg_trait3)

    return render_template("dogs_list.html",
                            pos_traits=pos_traits, 
                            neg_traits=neg_traits)

if __name__ == "__main__":

    #have to set debut=True to use debugger tool below
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(host="0.0.0.0")