from flask import Flask, render_template, request, jsonify, redirect, url_for, session, flash
from dotenv import load_dotenv
import os
from chatbot import Chatbot
from markdown import markdown
import pyrebase

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Firebase configuration
firebase_config = {
    "apiKey": os.getenv('FIREBASE_API_KEY'),
    "authDomain": os.getenv('FIREBASE_AUTH_DOMAIN'),
    "projectId": os.getenv('FIREBASE_PROJECT_ID'),
    "storageBucket": os.getenv('FIREBASE_STORAGE_BUCKET'),
    "messagingSenderId": os.getenv('FIREBASE_MESSAGING_SENDER_ID'),
    "appId": os.getenv('FIREBASE_APP_ID'),
    "databaseURL": os.getenv('FIREBASE_DATABASE_URL')
}

# Initialize Firebase
firebase = pyrebase.initialize_app(firebase_config)
auth = firebase.auth()

# Initialize chatbot
chatbot = Chatbot()

@app.route('/')
def home():
    if 'user' not in session:
        flash('Please login to access this page', 'info')
        return redirect(url_for('login'))
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        try:
            # Sign in with Pyrebase
            user = auth.sign_in_with_email_and_password(email, password)
            session['user'] = email
            session['token'] = user['idToken']
            flash('Successfully logged in!', 'success')
            return redirect(url_for('home'))
        except Exception as e:
            flash('Invalid email or password', 'danger')
            return redirect(url_for('login'))
            
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        try:
            # Create user with Pyrebase
            user = auth.create_user_with_email_and_password(email, password)
            session['user'] = email
            session['token'] = user['idToken']
            flash('Account created successfully!', 'success')
            return redirect(url_for('home'))
        except Exception as e:
            flash('Error creating account. Email might already be in use.', 'danger')
            return redirect(url_for('signup'))
            
    return render_template('signup.html')

@app.route('/chat', methods=['GET', 'POST'])
def chat():
    if 'user' not in session:
        if request.method == 'GET':
            flash('Please login to access this page', 'info')
            return redirect(url_for('login'))
        return jsonify({'error': 'Please login first'})
    
    if request.method == 'GET':
        return render_template('chat.html')
    
    try:
        message = request.json.get('message', '')
        response = chatbot.get_response(message)
        # Convert markdown to HTML and return
        html_response = markdown(response, extensions=['extra'])
        return jsonify({'response': html_response})
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/logout')
def logout():
    session.clear()
    flash('Successfully logged out!', 'info')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
