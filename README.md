
# Skill-Based Job Recommender System - Documentation

This file describes the structure, logic, and functionality of the Skill-Based Job Recommender System. It provides users with personalized job recommendations based on their preferred skill clusters, using unsupervised machine learning and real-time web scraping.

---

##  Contents of the System

1. **Job Scraping from Karkidi**
    - The `scraper.py` file scrapes job listings using BeautifulSoup from [Karkidi.com](https://www.karkidi.com).
    - Scraped data includes: job title, company, location, summary, and listed skills.

2. **Preprocessing & Clustering**
    - The `cluster_model.py` file preprocesses skill text data (cleaning, lowercasing, stemming).
    - TF-IDF vectorization is applied to convert text to numeric vectors.
    - K-Means Clustering groups job posts into skill-based clusters.
    - The model and vectorizer are saved as `job_model.pkl`.

3. **Streamlit Web Application**
    - The main UI is implemented in `streamlit_app.py`.
    - Users can:
      - Enter their email
      - Select clusters of interest based on skill summaries
      - View job recommendations matching their preferences
    - Matching jobs are presented with title, company, location, skills, and summary.

4. **User Preferences**
    - Preferences are stored in `user_preferences.json`, associating user emails with selected clusters.

5. **Pre-Clustered Dataset**
    - `clustered_jobs.csv` optionally contains preprocessed and clustered job postings for quick preview or offline testing.

---

##  How the System Works

**Step 1: Data Collection**
- The system scrapes jobs from the Karkidi site using `scraper.py`.

**Step 2: Skill Preprocessing**
- Extracted skills are cleaned, standardized, and vectorized.

**Step 3: Clustering**
- Unsupervised clustering groups jobs by similar skill requirements into 8 distinct clusters.

**Step 4: Cluster Labeling**
- Each cluster is described using dominant skills:

| Cluster ID | Top Skills                                       |
|------------|--------------------------------------------------|
| 0          | Data Analysis, Python, SQL                       |
| 1          | Machine Learning, Scikit-learn, TensorFlow       |
| 2          | Data Engineering, ETL, Spark                     |
| 3          | Web Development, JavaScript, React               |
| 4          | DevOps, AWS, Docker                              |
| 5          | Cybersecurity, Network Security                  |
| 6          | Business Intelligence, Power BI, Tableau         |
| 7          | Natural Language Processing, Transformers        |

**Step 5: User Interaction**
- Users interact via Streamlit to select clusters and view recommended jobs.

---

##  Project Structure

```
skill-job-recommender/
├── streamlit_app.py            # Streamlit web interface
├── scraper.py                  # Job scraper for Karkidi
├── cluster_model.py            # Preprocessing + clustering logic
├── clustered_jobs.csv          # Sample clustered dataset
├── job_model.pkl               # Trained model & TF-IDF vectorizer
├── user_preferences.json       # Stores user cluster choices
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

---

##  Dependencies

Install the required libraries via:

```
pip install -r requirements.txt
```

---

##  Running the Application

1. Clone the repository or download the project files.

2. Make sure you have Python 3.7+ installed.

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the Streamlit app:
```bash
streamlit run streamlit_app.py
```

---

