# app.py
from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
from utils.verify_token import verify_id_token
import os

app = Flask(__name__, template_folder="templates", static_folder="static")

# MongoDB (local)
mongo_uri = os.environ.get('MONGO_URI', 'mongodb://localhost:27017')
client = MongoClient(mongo_uri)
db = client['hackmate_db']
users_col = db['users']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup')
def signup_page():
    return render_template('signup.html')

@app.route('/login')
def login_page():
    return render_template('login.html')

@app.route('/dashboard')
def dashboard_page():
    return render_template('dashboard.html')

@app.route("/signup")
def signup():
    return "Signup Page"

@app.route("/profile")
def profile():
    return "Profile Page"

@app.route("/matches")
def matches():
    return render_template("matches.html")

@app.route("/chat")
def chat():
    return render_template("chat.html")


@app.route('/api/save_user', methods=['POST'])
def save_user():
    auth_header = request.headers.get('Authorization', None)
    if not auth_header:
        return jsonify({'error': 'Missing Authorization header'}), 401
    parts = auth_header.split()
    if parts[0].lower() != 'bearer' or len(parts) != 2:
        return jsonify({'error': 'Invalid Authorization header'}), 401
    id_token = parts[1]
    try:
        decoded = verify_id_token(id_token)
    except Exception as e:
        return jsonify({'error': 'Invalid token', 'message': str(e)}), 401

    uid = decoded.get('uid')
    data = request.json or {}
    email = data.get('email')
    displayName = data.get('displayName')

    # Upsert user (avoid duplicates)
    users_col.update_one(
        {'uid': uid},
        {'$set': {'uid': uid, 'email': email, 'name': displayName}},
        upsert=True
    )
    return jsonify({'ok': True, 'uid': uid})

@app.route("/api/profiles", methods=["GET"])
def get_profiles():
    # OPTIONAL: verify Firebase token if you want only logged-in users
    # decoded = verify_id_token(token)

    users = users_col.find(
        {},  # get all users
        {"_id": 0, "uid": 1, "name": 1, "skills": 1, "profile_pic_url": 1}
    )

    profiles = list(users)
    return jsonify(profiles)

if __name__ == '__main__':
    # For development only
    app.run(debug=True, host='0.0.0.0', port=5000)
