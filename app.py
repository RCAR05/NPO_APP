import os
from flask import Flask, redirect, url_for, session, request
import google_auth_oauthlib.flow
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests

app = Flask(Impact)
app.secret_key = os.environ.get('AIzaSyA8oqzWZMh6MQJ8PIgevFSnWuGlFpJy1O8')

# OAuth 2.0 setup
GOOGLE_CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID')
GOOGLE_CLIENT_SECRET = os.environ.get('GOOGLE_CLIENT_SECRET')
CLIENT_SECRETS_FILE = 'path_to_client_secret.json'  # Your downloaded JSON file from Google Cloud Console

@app.route('/')
def index():
    return 'Welcome to Non-Profit and Student Connection App'

@app.route('/login')
def login():
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE,
        scopes=['https://www.googleapis.com/auth/userinfo.profile', 'https://www.googleapis.com/auth/userinfo.email']
    )
    flow.redirect_uri = url_for('callback', _external=True)
    authorization_url, state = flow.authorization_url()
    session['state'] = state
    return redirect(authorization_url)

@app.route('/callback')
def callback():
    state = session['state']
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE,
        scopes=['https://www.googleapis.com/auth/userinfo.profile', 'https://www.googleapis.com/auth/userinfo.email'],
        state=state
    )
    flow.redirect_uri = url_for('callback', _external=True)
    authorization_response = request.url
    flow.fetch_token(authorization_response=authorization_response)
    credentials = flow.credentials
    request_session = google_requests.Request()
    id_info = id_token.verify_oauth2_token(credentials.id_token, request_session, 421196420306-uk83j1bct4rn08ioi6bsjcvgnmfgob5k.apps.googleusercontent.com)
    session['user_info'] = id_info
    return redirect(url_for('profile'))

@app.route('/profile')
def profile():
    user_info = session.get('user_info')
    if user_info:
        return f"User email: {user_info['email']}, User name: {user_info['name']}"
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
