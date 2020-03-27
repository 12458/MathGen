import flask
from flask import *

beer = Flask(__name__)

@beer.route("/")
def home():
    return render_template("home.html")

beer.run()
