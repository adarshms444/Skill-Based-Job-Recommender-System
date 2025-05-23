import os
import json
import joblib
from utils.notify import notify_user
from scraper import scrape_karkidi_jobs
from cluster_model import preprocess_skills

def load_seen_jobs(filename="seen_jobs.json"):
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            return set(json.load(f))
    return set()

def save_seen_jobs(jobs, filename="seen_jobs.json"):
    with open(filename, 'w') as f:
        json.dump(list(jobs), f, indent=4)

def load_user_preferences(filename="user_preferences.json"):
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            return json.load(f)
    return {}

def load_model(model_path="job_model.pkl"):
    """Loads the saved clustering model and vectorizer from disk."""
    return joblib.load(model_path)

def check_new_jobs():
    seen_jobs = load_seen_jobs()
    prefs = load_user_preferences()
    
    print("Scraping latest jobs...")
    df = scrape_karkidi_jobs(keyword="data science", pages=6)
    df["Skills"] = preprocess_skills(df["Skills"])

    print("Loading model...")
    model_data = load_model()
    model = model_data["model"]
    vectorizer = model_data["vectorizer"]

    print("Classifying new jobs...")
    skill_vectors = vectorizer.transform(df["Skills"])
    
    # Predict clusters using KMeans
    df["Cluster"] = model.predict(skill_vectors)

    # Fix columns for notification system
    df["id"] = df["Title"] + " - " + df["Company"]
    df["title"] = df["Title"]
    df["company"] = df["Company"]
    df["skills"] = df["Skills"]


    print("Clusters in new jobs:", df["Cluster"].value_counts())
    print("Notifying users...")
    new_jobs = df[~df["id"].isin(seen_jobs)]

    if new_jobs.empty:
        print("No new jobs to notify.")
    else:
        for _, job in new_jobs.iterrows():
            job_cluster = str(job["Cluster"])
            for user, settings in prefs.items():
                if job_cluster in settings.get("interests", []):
                    notify_user(user, job)

    save_seen_jobs(set(df["id"]))

if __name__ == "__main__":
    print(">>\nStarting daily job check...")
    check_new_jobs()

