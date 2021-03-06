import glob
import generator
from flask import Flask
from flask import request
from flask import render_template
from flask import redirect
from flask import send_file, current_app as app
database = "math_alevel_2019.db"
folder = "static"
path = "static/qn.pdf"
app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/submit", methods=["POST"])
def submit():
    saved_path = generator.generate(request.form['topic'], database, folder)
    return render_template("pdf.html", url=saved_path)


def cleanup(path):
    import os
    files = glob.glob(f'{path}/*')
    for f in files:
        os.remove(f)


if __name__ == "__main__":
    # Cleanup
    cleanup(folder)
    app.run(debug=True)
