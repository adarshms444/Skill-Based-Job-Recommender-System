#utils/notify.py

import smtplib
import os
import re
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
#
# Load credentials
load_dotenv()
GMAIL_USER = os.getenv("GMAIL_USER")
GMAIL_PASSWORD = os.getenv("GMAIL_PASSWORD")

def notify_user(email, job_list):
    if not job_list:
        print(f"ℹ️ No new jobs to send to {email}")
        return

    subject = f"🧠 New Job Alerts Matching Your Interests ({len(job_list)} Jobs)"

    html_body = f"<p>Hi {email},</p><p>Here are new job alerts matching your interests:</p>"

    for i, job in enumerate(job_list, start=1):
        job_link = job.get("Link", "#")
        if not job_link.startswith("http"):
            job_link = "https://www.karkidi.com" + job_link  # fallback

        # formatted_skills = ", ".join(job["Skills"].split())
        

        raw_skills = job.get("Skills", "")
        if "," not in raw_skills:
            skills_list = re.findall(r"\b(?:data science|machine learning|python|sql|r programming|tensorflow|kpi|product management|java|react|docker|aws|spark|power bi|tableau|excel|scikit-learn|nlp|transformers|cybersecurity|network security|graphql|next\.js|javascript|etl|hadoop)\b", raw_skills.lower())
        else:
            skills_list = [s.strip() for s in re.split(r"[•,;|]", raw_skills) if s.strip()]
        formatted_skills = ", ".join(skills_list)



        html_body += f"""
        <div style="border:1px solid #ccc; padding:15px; margin-bottom:15px; border-radius:10px;">
            <h3>🔹 Job {i}: {job['Title']}</h3>
            <p><b>🏢 Company:</b> {job['Company']}<br>
               <b>📍 Location:</b> {job.get('Location', 'N/A')}<br>
               <b>💼 Experience:</b> {job.get('Experience', 'N/A')}<br>
               <b>🧠 Skills:</b> {formatted_skills}<br>
               <b>📄 Summary:</b> {job.get('Summary', 'No summary provided.')[:300]}...</p>
            <p>
               <a href="{job_link}" target="_blank" style="
                   background-color:#4CAF50;
                   color:white;
                   padding:10px 15px;
                   text-decoration:none;
                   border-radius:5px;
                   font-weight:bold;
                   display:inline-block;">
                   👉 View Full Job
               </a>
            </p>
        </div>
        """

    html_body += "<p>Best of luck!<br>– Your Job Recommender System 🤖</p>"

    # Compose the HTML email
    msg = MIMEMultipart("alternative")
    msg["From"] = GMAIL_USER
    msg["To"] = email
    msg["Subject"] = subject
    msg.attach(MIMEText(html_body, "html"))  # 👈 HTML Part only

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(GMAIL_USER, GMAIL_PASSWORD)
        server.send_message(msg)
        server.quit()
        print(f"✅ HTML email sent to {email} with {len(job_list)} jobs.")
    except Exception as e:
        print(f"❌ Failed to send email to {email}: {e}")


