from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import session
from flask import url_for
from flask_pymongo import PyMongo




app = Flask(__name__)

# events = [
#         {"event":"Deltamath Assignment 1", "date":"2020-09-25"},
#         {"event":"Fall MP1 Project", "date": "2020-10-9"},
#         {"event":"Unit 1 Extravaganza", "date":"20-10-7"}
#     ]

app.config['MONGO_DBNAME'] = 'database'
app.config['MONGO_URI'] = 'mongodb+srv://admin:GQy9fnodZrEIN9a6@cluster0.7u0fo.mongodb.net/database?retryWrites=true&w=majority'


mongo = PyMongo(app)


@app.route('/')
@app.route('/index')

def index():
    session['username']='Ileini'
    events = mongo.db.events
    # print(collection)
    events = events.find({})
    print(events)
    return render_template('welcome.html', events=events)
    

@app.route('/events/add', methods = ['GET', 'POST'])

def add():
    if request.method == "GET":
        return render_template('add.html')
    else:
        event_name = request.form['event_name']
        event_date = request.form['event_date']
    
        collection = mongo.db.events
        

        collection.insert({'event': event_name, 'date': event_date}) 
        events = collection.find({})
        # print(events)   
        return render_template("announcements.html", events=events)

#signup
@app.route('/signup', methods = ['GET', 'POST'])

def signup():
    if request.method == 'POST':
        users = mongo.db.users
        existing_user = users.find_one({'name' : request.form['username']})

        if existing_user is None:
            users.insert({'name' : request.form['username'], 'password' : request.form['password']})
            session['username'] = request.form['username']
            return redirect(url_for('index'))
        
        return 'That username already exists! Try logging in!'
    
    return render_template('signup.html')

@app.route('/announcements', methods = ['GET', 'POST'])

def announcements():
    # session['username']='Ileini'
    events = mongo.db.events
    # print(collection)
    events = events.find({})
    # print(events)
    return render_template('announcements.html', events=events)
# events = events

@app.route('/login', methods = ['GET', 'POST'])

def login():
    users = mongo.db.users
    login_user = users.find_one({"name": request.form['username']})

    if login_user:
        if request.form['password'] == login_user['password']:
            session['username'] = request.form['username']
            return redirect(url_for('announcements'))
    
    return 'Invalid username/password combination.'


app.secret_key = 'uo4xbZQnqxeFcpP9'
