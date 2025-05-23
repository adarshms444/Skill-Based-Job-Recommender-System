# job_classifier.py

from model_utils import load_model
from cluster_model import preprocess_skills
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

def classify_jobs(df, model_path="job_model.pkl"):
    data = load_model(model_path)
    model = data["model"]
    vectorizer = data["vectorizer"]
    train_vectors = data["vectors"]
    train_labels = data["labels"]

    df = df.copy()
    skills_processed = preprocess_skills(df["Skills"])
    new_vectors = vectorizer.transform(skills_processed).toarray()

    # Compute centroids from training vectors
    cluster_centers = []
    for i in range(max(train_labels) + 1):
        cluster_vectors = train_vectors[train_labels == i]
        cluster_centers.append(cluster_vectors.mean(axis=0))

    # Assign each new job to the nearest cluster
    assigned_clusters = []
    for vec in new_vectors:
        similarities = [cosine_similarity([vec], [center])[0][0] for center in cluster_centers]
        assigned_clusters.append(similarities.index(max(similarities)))

    df["Cluster"] = assigned_clusters
    return df
