from flask import Flask, Response, jsonify, make_response, redirect, render_template, request, send_from_directory, url_for
# generate jwt token import
import jwt
from time import time
import os
import asyncio
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

app = Flask(__name__, static_folder='spotify')
cred = credentials.Certificate('./spotify/serviceAccountKey.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://spotify-d5016-default-rtdb.europe-west1.firebasedatabase.app'
})
# 
jwt_token = "None"
def render_set( url ):
    with open( url ) as f:
        return Response(f.read(), mimetype="text/html") 
def generate_jwt_token(username):
    seconds_now = time()
    jwt_secret = os.environ.get('JWT_SECRET', 'izzy')
    token = {
        "username": username,
        "iat": seconds_now -1,
        "exp": seconds_now + 7200 #30000
    }
    return jwt.encode( token,jwt_secret, algorithm="HS256" )
def ok_jwt_token(token):
    try:
        jwt_secret = os.environ.get('JWT_SECRET', 'izzy')
        decoded_token = jwt.decode(token, jwt_secret, algorithms=['HS256'])
        return True, decoded_token
    except jwt.ExpiredSignatureError:
        return False, "Token has expired."
    except jwt.InvalidTokenError:
        return False, "Invalid token."

@app.route('/')
def home():
    return render_set( './spotify/index.html' )   

@app.route('/createplaylist', methods=['POST'])
def create_playlist():
    # Get the username from the request cookies
    username = request.cookies.get('username')
    # return jwt_token
    global jwt_token
    is_valid, decoded = ok_jwt_token(jwt_token)
    if is_valid :
        if request.method == 'POST' and username:
            # Get a reference to the root of the database
            playlist_ref = db.reference( 'playlists/'+username )   
            # Query users where username and password are equal
            # Get all child nodes
            all_playlists = playlist_ref.get()
            # Process the child nodes
            if all_playlists and request.json['start'] ==True:
                return jsonify( all_playlists )
            elif request.json['start'] ==True:
                return jsonify( { 'number' : 0 } )
            if all_playlists:
                all_playlists['number'] = all_playlists['number'] + 1
                number = all_playlists['number']
                save_playlists( playlist_ref, "number" , all_playlists['number'] )
                save_playlists( playlist_ref, f'{number}' , [0] )
                return jsonify( all_playlists )
            else:
                data = { 'number' : 1 }
                # Set the data with a specific ID
                playlist_ref.set(data)
                save_playlists( playlist_ref, "1", [0] )
                return jsonify( data )
        return None
    else:
        return jsonify({'error': 'Token has expired'}), 401

def save_playlists( playlist_ref, dir, data ):
    playlist_ref.child( dir ).set( data )


@app.route('/index', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        users_ref = db.reference( 'users' )
        # Query users where username and password are equal
        query = users_ref.order_by_child('username').equal_to( username ).get()
        # Filter the query results by password
        results = [ user for user in query.values() if user.get('password') == password ]
        
        if len(results) != 0:
            # return {"token": }
            global jwt_token
            jwt_token = generate_jwt_token( username )
            # Set the "username" cookie
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


@app.route('/playlistsonds', methods=['POST'])
def playlistsond():
    # Get the username from the request cookies
    username = request.cookies.get('username')
    # return jwt_token
    global jwt_token
    is_valid, decoded = ok_jwt_token(jwt_token)
    if is_valid :
        if request.method == 'POST' and username:
            # Get a reference to the root of the database
            number = request.json['number']
            path = 'playlists/'+ username + '/'+ f'{number}'
            playlist_ref = db.reference( path )   
            all_playlists = playlist_ref.get()
            # Process the child nodes
            if all_playlists:
                return jsonify( all_playlists )
            return None
        return None
    else:
        return jsonify({'error': 'Token has expired'}), 401
    

@app.route('/songs', methods=['POST'])
def get_all_sonds():
    # Get the username from the request cookies
    username = request.cookies.get('username')
    # return jwt_token
    global jwt_token
    is_valid, decoded = ok_jwt_token(jwt_token)
    if is_valid :
        if request.method == 'POST' and username:
            # Get a reference to the root of the database
            playlist_ref = db.reference( 'songs' )   
            all_playlists = playlist_ref.get()
            # Process the child nodes
            if all_playlists:
                return jsonify( all_playlists )
            return None
        return None
    else:
        return jsonify({'error': 'Token has expired'}), 401
       

@app.route('/addsong', methods=['POST'])
def get_add_sond():
    # Get the username from the request cookies
    # return jwt_token
    global jwt_token
    is_valid, decoded = ok_jwt_token(jwt_token)
    if is_valid :
        username = request.cookies.get('username')
        number = request.cookies.get('number')
        if request.method == 'POST' and username and number:
            # Get a reference to the root of the database
            path = 'playlists/'+ username + '/'+ f'{number}'
            playlist_ref = db.reference( path )   
            all_playlists = playlist_ref.get()
            # Process the child nodes
            if all_playlists:
                data = {
                    'name' : request.json['name'],
                    'filename' : request.json['filename'],
                    'description' : request.json['description'],
                }
                id = request.json['filename'].strip().replace(" ", "").replace(".", "")
                save_playlists( playlist_ref, id, data ) 

                path = 'playlists/'+ username + '/'+ f'{number}/'
                playlist_ref = db.reference( path )   
                all_playlists = playlist_ref.get()

                return jsonify( all_playlists )
            return None
        return None
    else:
        return jsonify({'error': 'Token has expired'}), 401
        


@app.route('/findsongs', methods=['POST'])
def get_find_sond():
    
    # return jwt_token
    global jwt_token
    is_valid, decoded = ok_jwt_token(jwt_token)
    if is_valid :
        # Get the username from the request cookies
        username = request.cookies.get('username')
        if request.method == 'POST' and username:
            # Get a reference to the root of the database
            playlist_ref = db.reference( 'songs' )   
            all_playlists = playlist_ref.get()
            find_song = request.json['find_song'].lower()
            data =[]
            for  value in all_playlists: 
                name = value['name'].lower()
                description = value['description'].lower()
                if find_song in name:
                    data.append( value )
                elif find_song in description:
                    data.append( value )
            return jsonify( data )
        return None
    else:
        return jsonify({'error': 'Token has expired'}), 401

@app.route('/spotify/css/<path:filename>')
def serve_css(filename):
    return send_from_directory('css', filename)

@app.route('/spotify/js/<path:filename>')
def serve_js(filename):
    return send_from_directory('js', filename)

@app.route('/spotify/mp3/<path:filename>')
def serve_mp3(filename):
    return send_from_directory('mp3', filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0')