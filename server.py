import generator
from flask import Flask  # Class
from flask import request
from flask import render_template  # Function
from flask import redirect
from flask import send_file, current_app as app
# Object[class must init while obj has already created]
#from flask import request

app = Flask(__name__)  # __main__ server.py is the main function
# anything that have __ __ they are keyword and they are already defined

# Make this a ViewFunction
# @app.route("/") Python syntax : do something before the function is invoked -- decorator
@app.route("/")
def home():
    return render_template("index.html")

path = "static/qn.pdf"
@app.route("/submit", methods=["POST"])
def submit():
    # Python dictionary object
    global path
    path = generator.generate(request.form['topic'])
    print(path)
    return redirect('static/', code=302)

@app.route('/static/')
def show_static_pdf():
    global path
    print(path)
    with open(path, 'rb') as static_file:
        print(static_file.read())
        return send_file(static_file, attachment_filename='file.pdf')


app.run()  # infinite loop
