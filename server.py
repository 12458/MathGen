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
    path = generator.generate(request.form['topic'], "math_alevel_2019.db", "static/qn.pdf")
    print(path)
    return render_template("pdf.html", url=path)


# @app.route('/static/')
# def show_static_pdf():
#     global path
#     print(path)
#     return render_template("pdf.html", url=path)


app.run()
