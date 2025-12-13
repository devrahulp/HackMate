# app.py
from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
from bson import ObjectId
import os

from firebase_admin import auth
from utils.verify_token import verify_id_token
from utils.db import users, requests as requests_col, notifications as notifications_col

# ---------------- APP CONFIG ----------------
app = Flask(__name__, template_folder="templates", static_folder="static")

# ---------------- MONGODB ----------------
mongo_uri = os.environ.get("MONGO_URI", "mongodb://localhost:27017")
client = MongoClient(mongo_uri)
db = client["hackmate_db"]
users_col = db["users"]

# ---------------- HOME ----------------
@app.route("/")
def index():
    return render_template("index.html")

# ---------------- AUTH PAGES ----------------
@app.route("/signup")
def signup_page():
    return render_template("signup.html")

@app.route("/login")
def login_page():
    return render_template("login.html")

# ---------------- DASHBOARD ----------------
@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@app.route("/edit-profile")
def edit_profile():
    return render_template("edit_profile.html")

@app.route("/profile")
def profile():
    return "Profile Page"

@app.route("/matches")
def matches():
    return render_template("matches.html")

@app.route("/chat")
def chat():
    return render_template("chat.html")

@app.route("/explore")
def explore():
    return render_template("explore.html")

@app.route("/requests")
def requests_page():
    return render_template("requests.html")

# ---------------- API: SAVE USER (Firebase) ----------------
@app.route("/api/save_user", methods=["POST"])
def save_user():
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        return jsonify({"error": "Missing Authorization header"}), 401

    parts = auth_header.split()
    if parts[0].lower() != "bearer" or len(parts) != 2:
        return jsonify({"error": "Invalid Authorization header"}), 401

    id_token = parts[1]
    decoded = verify_id_token(id_token)

    uid = decoded.get("uid")
    data = request.json or {}

    users_col.update_one(
        {"uid": uid},
        {
            "$set": {
                "uid": uid,
                "email": data.get("email"),
                "name": data.get("displayName"),
            }
        },
        upsert=True,
    )

    return jsonify({"ok": True, "uid": uid})

# ---------------- API: SAVE PROFILE ----------------
@app.route("/api/save-profile", methods=["POST"])
def save_profile():
    token = request.headers.get("Authorization")
    user = verify_id_token(token)

    data = request.json or {}
    data["uid"] = user["uid"]
    data["email"] = user.get("email")

    users_col.update_one(
        {"uid": user["uid"]},
        {"$set": data},
        upsert=True,
    )

    return jsonify({"status": "success"})

# ---------------- API: GET LOGGED-IN PROFILE ----------------
@app.route("/api/profile")
def get_profile():
    token = request.headers.get("Authorization")
    user = verify_id_token(token)

    profile = users_col.find_one(
        {"uid": user["uid"]},
        {"_id": 0},
    )

    return jsonify(profile or {})

# ---------------- API: GET PROFILES (HOMEPAGE) ----------------
@app.route("/api/profiles")
def get_profiles():
    cursor = users_col.find(
        {},
        {
            "_id": 1,
            "name": 1,
            "college": 1,
            "skills": 1,
            "profile_pic": 1,
        },
    ).limit(10)

    profiles = []
    for user in cursor:
        profiles.append(
            {
                "id": str(user["_id"]),
                "name": user.get("name", "Anonymous"),
                "college": user.get("college", "N/A"),
                "skills": user.get("skills", []),
                "profile_pic": user.get("profile_pic", ""),
            }
        )

    return jsonify(profiles)

# ---------------- API: SUGGESTIONS ----------------
@app.route("/api/suggestions")
def suggestions():
    token = request.headers.get("Authorization")
    user = auth.verify_id_token(token)

    profiles = users_col.find({"uid": {"$ne": user["uid"]}}, {"_id": 0})
    return jsonify(list(profiles))

# ---------------- API: NOTIFICATIONS ----------------
@app.route("/api/notifications")
def get_notifications():
    token = request.headers.get("Authorization")
    user = auth.verify_id_token(token)

    notes = notifications_col.find({"uid": user["uid"]}, {"_id": 0})
    return jsonify(list(notes))

# ---------------- RUN SERVER ----------------
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)