
import streamlit as st
import pandas as pd
import joblib
import json
from datetime import datetime
import re

from cluster_model import preprocess_skills
from scraper import scrape_karkidi_jobs

# Set layout and title
st.set_page_config(page_title="🔍 Skill-Based Job Recommender", layout="wide")

# Load model
model_data = joblib.load("job_model.pkl")
model = model_data["model"]
vectorizer = model_data["vectorizer"]

# Cluster labels
cluster_labels = {
    0: "Data Analysis, Python, SQL",
    1: "Machine Learning, Scikit-learn, TensorFlow",
    2: "Data Engineering, ETL, Spark",
    3: "Web Development, JavaScript, React",
    4: "DevOps, AWS, Docker",
    5: "Cybersecurity, Network Security",
    6: "Business Intelligence, Power BI, Tableau",
    7: "Natural Language Processing, Transformers"
}
label_to_cluster = {v: k for k, v in cluster_labels.items()}

# Load and save user preferences
def load_preferences():
    try:
        with open("user_preferences.json") as f:
            return json.load(f)
    except:
        return {}

def save_preferences(prefs):
    with open("user_preferences.json", "w") as f:
        json.dump(prefs, f, indent=4)

# 📅 Date & Time
st.markdown(
    f"<div style='text-align:right;font-size:14px;'>📅 <b>{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</b></div>",
    unsafe_allow_html=True
)

# Title
st.markdown("<h1 style='font-size: 40px;'>🤖 Skill-Based Job Recommender</h1>", unsafe_allow_html=True)
st.markdown("---")

# User Input
email = st.text_input("📧 Enter your email", placeholder="you@example.com")

selected_labels = st.multiselect(
    "🎯 Select your interested clusters",
    options=list(cluster_labels.values()),
    help="These clusters represent types of job skill sets."
)

col1, col2 = st.columns(2)

# ✅ Save preferences
with col1:
    if st.button("✅ Save Preferences"):
        if email and selected_labels:
            prefs = load_preferences()
            prefs[email] = {"interests": [str(label_to_cluster[label]) for label in selected_labels]}
            save_preferences(prefs)
            st.success("🎉 Preferences saved. You’ll receive job alerts daily.")
        else:
            st.warning("⚠️ Please enter your email and select at least one cluster.")

# ✅ Fetch jobs and show results
with col2:
    if st.button("📥 Fetch Jobs Now"):
        if email and selected_labels:
            st.info("⏳ Scraping jobs. Please wait...")
            df = scrape_karkidi_jobs("data science", pages=3)
            df["Skills"] = preprocess_skills(df["Skills"])
            df["Cluster"] = model.predict(vectorizer.transform(df["Skills"]))

            selected_clusters = [label_to_cluster[label] for label in selected_labels]
            filtered = df[df["Cluster"].isin(selected_clusters)]

            if not filtered.empty:
                st.markdown(f"### 🔔 Recommended Jobs for <code>{email}</code>", unsafe_allow_html=True)

                for _, row in filtered.iterrows():
                    # ✅ Format skills with multiple separators
                    raw_skills = row.get("Skills", "")
                    if isinstance(raw_skills, str):
                        if "," not in raw_skills:
                           skills_list = re.findall(r"\b(?:data science|machine learning|python|sql|r programming|tensorflow|kpi|product management|java|react|docker|aws|spark|power bi|tableau|excel|scikit-learn|nlp|transformers|cybersecurity|network security|graphql|next\.js|javascript|etl|hadoop)\b", raw_skills.lower())
                        else:
                           skills_list = [s.strip() for s in re.split(r"[•,;|]", raw_skills) if s.strip()]
                    else:
                        skills_list = list(raw_skills)

                    formatted_skills = "\n".join([f"• {s}" for s in skills_list])

                    # ✅ Handle individual summary
                    summary = row.get("Summary", "")
                    if not isinstance(summary, str) or summary.strip() == "" or pd.isna(summary):
                        summary = "No summary provided."

                    # ✅ Display job card
                    st.markdown(f"""
<div style='padding: 15px; border: 1px solid #ddd; border-radius: 10px; margin-bottom: 15px; background-color: #f9f9f9;'>
    <h4 style='margin-bottom:5px;'>{row['Title']}</h4>
    <i>{row['Company']}</i><br><br>
    📍 <b>Location:</b> {row.get('Location', 'N/A')}<br><br>
    💼 <b>Experience:</b> {row.get('Experience', 'Not specified')}<br><br>
    🧠 <b>Skills:</b> {', '.join(skills_list)}<br><br>
    📋 {summary}

</div>
""", unsafe_allow_html=True)

            else:
                st.warning("🚫 No jobs found for your selected clusters.")
        else:
            st.warning("⚠️ Please enter your email and select at least one cluster.")



