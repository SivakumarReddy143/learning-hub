from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import pyrebase
import os
from dotenv import load_dotenv
from chatbot import Chatbot

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'your_secret_key')  # Use environment variable for secret key

# Initialize chatbot
chatbot = Chatbot()

# 🔥 Firebase Configuration
firebase_config = {
    "apiKey": os.getenv('FIREBASE_API_KEY', 'AIzaSyBx0qex-Oygbk5hT93A8qZW_vofoxzR-PI'),
    "authDomain": os.getenv('FIREBASE_AUTH_DOMAIN', 'learning-hub-a0333.firebaseapp.com'),
    "projectId": os.getenv('FIREBASE_PROJECT_ID', 'learning-hub-a0333'),
    "storageBucket": os.getenv('FIREBASE_STORAGE_BUCKET', 'learning-hub-a0333.firebasestorage.app'),
    "messagingSenderId": os.getenv('FIREBASE_MESSAGING_SENDER_ID', '634711985625'),
    "appId": os.getenv('FIREBASE_APP_ID', '1:634711985625:web:b161c2b4bf83fb86081dc8'),
    "measurementId": os.getenv('FIREBASE_MEASUREMENT_ID', 'G-PVHLBY36YJ'),
    "databaseURL": os.getenv('FIREBASE_DATABASE_URL', 'https://learning-hub-a0333-default-rtdb.firebaseio.com')
}

firebase = pyrebase.initialize_app(firebase_config)
auth = firebase.auth()

@app.route('/')
def home():
    return render_template('home.html') if 'user' in session else redirect(url_for('login'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            user = auth.create_user_with_email_and_password(email, password)
            flash("Account created successfully! Please log in.", "success")
            return redirect(url_for('login'))
        except Exception as e:
            flash("Error: " + str(e), "danger")
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            user = auth.sign_in_with_email_and_password(email, password)
            session['user'] = user['idToken']
            flash("Logged in successfully!", "success")
            return redirect(url_for('home'))
        except Exception as e:
            flash("Login failed: " + str(e), "danger")
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    flash("You have been logged out.", "info")
    return redirect(url_for('login'))

@app.route('/chat')
def chat_page():
    if 'user' not in session:
        flash("Please log in to access the chat.", "warning")
        return redirect(url_for('login'))
    return render_template('chat.html')

@app.route('/chat', methods=['POST'])
def chat():
    if 'user' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    data = request.get_json()
    message = data.get('message', '')
    
    if not message:
        return jsonify({'error': 'No message provided'}), 400
    
    try:
        response = chatbot.get_response(message)
        return jsonify({'response': response})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)  # Set debug=False for production
