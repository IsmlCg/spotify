from flask import Flask, Response, redirect, render_template, request, send_from_directory, url_for
# generate jwt token import
import jwt
from time import time
import os
# import database firebase
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
app = Flask(__name__, static_folder='spotify')
cred = credentials.Certificate('./spotify/serviceAccountKey.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://spotify-d5016-default-rtdb.europe-west1.firebasedatabase.app'
})
# 
def render_set( url ):
    with open( url ) as f:
        return Response(f.read(), mimetype="text/html") 
    
def generate_jwt_token(username):
    seconds_now = time()
    return jwt.encode(
        {   "username": username, 
            "iat": seconds_now,
            "exp": seconds_now + 30000
        },
        os.environ.get('JWT_SECRET'),
        algorithm="HS256"
    )

@app.route('/')
def home():
    return render_set( './spotify/index.html' )   

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        # Get a reference to the root of the database
        root = db.reference()
        users_ref = db.reference( 'users' )
        # Query users where username and password are equal
        query = users_ref.order_by_child('username').equal_to( username ).get()
        # Filter the query results by password
        results = [ user for user in query.values() if user.get('password') == password ]
        
        if len(results) != 0:
            # return {"token": generate_jwt_token( username )}
            return render_set( './spotify/html/main.html' ) 
        else:
            sms = "Invalid username or password"
            with open('./spotify/index.html') as f:
                return Response(f.read().replace('{{ sms }}', sms), mimetype='text/html')
    elif request.method == 'GET':
        return render_set( './spotify/index.html' ) 

@app.route('/signup', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        # Get a reference to the root of the database
        users_ref = db.reference( 'users' )
        fullname = request.form.get('fullname')
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Query users where username and password are equal
        query = users_ref.order_by_child('username').equal_to( username ).get()
        if len(query) == 0:
            user_data = {
                'fullname' : fullname,
                'username' : username,
                'password' : password
            }
            new_user = users_ref.push(user_data)
            return render_set( './spotify/index.html' ) 
        else:
            sms = "Username exist."
            with open('./spotify/html/signup.html') as f:
                return Response(f.read().replace('{{ sms }}', sms), mimetype='text/html')
    elif request.method == 'GET':
        return render_set( './spotify/html/signup.html' ) 
    
@app.route('/spotify/css/<path:filename>')
def serve_css(filename):
    return send_from_directory('css', filename)
# 

    
if __name__ == '__main__':
    app.run(host='0.0.0.0')