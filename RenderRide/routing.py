from flask import Flask, request, redirect, url_for, render_template, jsonify, session
import os

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-key-change-in-production')

def login_required(f):
    def wrapper(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    wrapper.__name__ = f.__name__
    return wrapper

@app.route('/')
def index():
    return render_template('landingpage.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username'] 
    if username:
        session['username'] = username
        return redirect(url_for('aboutme'))
    
    return render_template('landingpage.html', error="Please enter a username.")

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/aboutme')
@login_required
def aboutme():
    return render_template('aboutme.html')

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/chat')
@login_required
def chat():
    return render_template('chat.html')

@app.route('/chat', methods=['POST'])
@login_required
def chat_message():
    user_message = request.json.get('message')
    bot_response = f"Echo: {user_message}"
    return jsonify(response=bot_response)

if __name__ == "__main__":
    app.run(debug=True)