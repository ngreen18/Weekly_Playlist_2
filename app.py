# ---- YOUR APP STARTS HERE ----
# -- Import section --
import os
import app
from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import session
from flask import url_for
from flask_pymongo import PyMongo


# -- Initialization section --
app = Flask(__name__)

app.secret_key = '_5#y2L"F4Q8z\n\xec]/'

# name of database
app.config['MONGO_DBNAME'] = 'Database#1'

# URI of database
app.config['MONGO_URI'] = 'mongodb+srv://Admin:iS5zXAaPm9vGigov@cluster0.dpy0j.mongodb.net/Database#1?retryWrites=true&w=majority'

mongo = PyMongo(app)

# -- Routes section --
# INDEX

@app.route('/')
@app.route('/index', methods = {"GET", "POST"})
def index():
    session["username"] = "Nathaniel"
    collection = mongo.db.question1
    all_data = collection.find({})
    all_data_2 = collection.find({})
    if request.method == 'GET':
        return render_template('/index.html')
    elif request.method == 'POST':
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        question_1 = request.form["question#1"]
        question_2 = request.form["question#2"]
        Question_1 = mongo.db.question1
        Question_1.insert(
            {"FirstName": first_name, "LastName": last_name, "Question1": question_1, "Question2": question_2} )
        return render_template('/index.html', all_data = all_data, all_data_2 = all_data_2)

#SIGN UP

@app.route("/signup", methods = ["POST", "GET"])

def signup():
    if request.method == "POST":
        users = mongo.db.user
        existing_user = users.find_one({"name": request.form["username"]})

        if existing_user is None:
            users.insert({"name": request.form["username"], "password": request.form['password']})
            session["username"] = request.form["username"]
            return redirect(url_for("index"))

        return "That username already exists. Try loggin in"

    return render_template('/signup.html')

#Log In

@app.route('/login', methods=['POST'])

def login():
    users = mongo.db.user
    login_user = users.find_one({'name' : request.form['username']})

    if login_user:
        if request.form['password'] == login_user['password']:
            session['username'] = request.form['username']
            return redirect(url_for('index'))

    return 'Invalid username/password combination'

#Log Out

@app.route('/logout', methods = ["POST", "GET"])
def logout():
    session.clear()
    return redirect('/')