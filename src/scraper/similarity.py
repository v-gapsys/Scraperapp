from .models import JobListing
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class SimilarityAnalyzer:
    """Class for analyzing similarity between job listings."""

    def __init__(self):
        self.vectorizer = TfidfVectorizer()

    def vectorize_job(self, job):
        """Convert job data into a text string for vectorization."""
        if isinstance(job, dict):
            # For reference job (dictionary)
            title = job.get('Darbo pobūdis', '')
            location = job.get('Darbo vieta (miestas)', '')
            salary = job.get('Pageidaujamas atlyginimas', '')
            experience = job.get('Turima patirtis', '')
            description = job.get('Darbo aprašymas', '')
        else:
            # For JobListing objects
            title = job.title
            location = job.location
            salary = str(job.salary) if job.salary else ''
            experience = job.details.get('Turima patirtis', '')
            description = job.details.get('Darbo aprašymas', '')

        # Repeat the title multiple times to give it more weight in TF-IDF
        # This makes the profession match more important than vague terms
        return f"{title} {title} {title} {location} {salary} {experience} {description}"

    def compute_similarity(self, reference_job, offered_jobs):
        """Compute similarity between reference job and offered jobs."""
        reference_text = self.vectorize_job(reference_job)
        offered_texts = [self.vectorize_job(job) for job in offered_jobs]
        all_texts = [reference_text] + offered_texts
        tfidf_matrix = self.vectorizer.fit_transform(all_texts)
        similarity_scores = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:])
        # Debug print statements
        print("\nVectorized Reference Job Text:")
        print(reference_text)
        print("\nVectorized Offered Job Texts:")
        for i, text in enumerate(offered_texts):
            print(f"Job {i+1}: {text}")
        print("\nSimilarity Scores:")
        for i, score in enumerate(similarity_scores[0]):
            print(f"Job {i+1}: {score:.4f}")
        # Return offered jobs with their similarity scores, sorted by similarity in descending order
        return sorted([(offered_jobs[i], similarity_scores[0][i]) for i in range(len(offered_jobs))], key=lambda x: x[1], reverse=True) 