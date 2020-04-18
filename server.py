import generator
from flask import Flask
from flask import request
from flask import render_template
from flask import redirect
from flask import send_file, current_app as app


app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


path = "static/qn.pdf"
@app.route("/submit", methods=["POST"])
def submit():
    global path
    path = generator.generate(request.form['topic'])
    print(path)
    return path


@app.route('/static/')
def show_static_pdf():
    global path
    print(path)
    with open(path, 'rb') as static_file:
        print(static_file.read())
        return send_file(static_file, attachment_filename='file.pdf')


app.run()
