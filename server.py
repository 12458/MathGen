import generator
from flask import Flask  # Class
from flask import render_template  # Function
# Object[class must init while obj has already created]
from flask import request

app = Flask(__name__)  # __main__ server.py is the main function
# anything that have __ __ they are keyword and they are already defined

# Make this a ViewFunction
# @app.route("/") Python syntax : do something before the function is invoked -- decorator
@app.route("/")
def home():
    return render_template("index.html")


@app.route("/submit", methods=["POST"])
def submit():
    # Python dictionary object
    return generator.generate(str(request.form['topic']))


app.run()  # infinite loop
