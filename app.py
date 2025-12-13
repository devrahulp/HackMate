# app.py
from flask import Flask, render_template, request, jsonify,session
from pymongo import MongoClient
from utils.verify_token import verify_id_token
import os
from firebase_admin import auth
from utils.db import users, requests, notifications

app = Flask(__name__, template_folder="templates", static_folder="static")

# MongoDB (local)
mongo_uri = os.environ.get('MONGO_URI', 'mongodb://localhost:27017')
client = MongoClient(mongo_uri)
db = client['hackmate_db']
users_col = db['users']



@app.route("/api/notifications")
def notifications():
    token = request.headers.get("Authorization")
    user = auth.verify_id_token(token)

    notes = notifications.find({"uid": user["uid"]})
    return jsonify(list(notes))
@app.route("/requests")
def requests_page():
    return render_template("requests.html")
@app.route("/api/suggestions")
def suggestions():
    token = request.headers.get("Authorization")
    user = auth.verify_id_token(token)

    profiles = users.find({"uid": {"$ne": user["uid"]}})
    return jsonify(list(profiles))



@app.route("/api/save-profile", methods=["POST"])
def save_profile():
    token = request.headers.get("Authorization")
    user = verify_firebase_token(token)

    data = request.json
    data["uid"] = user["uid"]
    data["email"] = user["email"]

    users.update_one(
        {"uid": user["uid"]},
        {"$set": data},
        upsert=True
    )

    return jsonify({"status": "success"})
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup')
def signup_page():
    return render_template('signup.html')

@app.route('/login')
def login_page():
    return render_template('login.html')

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@app.route("/edit-profile")
def edit_profile():
    return render_template("edit_profile.html")

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

@app.route("/api/profile")
def get_profile():
    token = request.headers.get("Authorization")
    user = verify_firebase_token(token)

    profile = users.find_one(
        {"uid": user["uid"]},
        {"_id": 0}  # remove Mongo _id
    )

    return jsonify(profile or {})

if __name__ == '__main__':
    # For development only
    app.run(debug=True, host='0.0.0.0', port=5000)
