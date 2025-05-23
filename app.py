# app.py

from flask import Flask, render_template, request, redirect, url_for, session
import json
import pandas as pd
import os

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Replace with a real secret key
USER_PREF_FILE = "user_preferences.json"
JOBS_FILE = "clustered_jobs.csv"

def load_users():
    if os.path.exists(USER_PREF_FILE):
        with open(USER_PREF_FILE, "r") as f:
            return json.load(f)
    return {}

def save_users(data):
    with open(USER_PREF_FILE, "w") as f:
        json.dump(data, f, indent=2)

@app.route('/')
def home():
    if "username" in session:
        return redirect(url_for("dashboard"))
    return render_template("index.html")

@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        interests = request.form.getlist("interests")  # ["0", "2", "4"]

        users = load_users()
        users[username] = {"interests": interests}
        save_users(users)

        session["username"] = username
        return redirect(url_for("dashboard"))

    # Assuming clusters 0 to 4
    clusters = [str(i) for i in range(5)]
    return render_template("register.html", clusters=clusters)

@app.route('/dashboard')
def dashboard():
    if "username" not in session:
        return redirect(url_for("home"))

    username = session["username"]
    users = load_users()
    user_clusters = users[username]["interests"]

    df = pd.read_csv(JOBS_FILE) if os.path.exists(JOBS_FILE) else pd.DataFrame()
    if "Cluster" in df.columns:
        df = df[df["Cluster"].astype(str).isin(user_clusters)]

    return render_template("dashboard.html", username=username, jobs=df.to_dict(orient="records"))

@app.route('/logout')
def logout():
    session.pop("username", None)
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000)

