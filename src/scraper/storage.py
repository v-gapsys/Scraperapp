"""
Storage handlers for saving scraped data.
"""
import pandas as pd
from typing import List
from .models import JobListing
from .config import OUTPUT_FILENAME

class Storage:
    """Base storage class."""
    def save(self, jobs: List[JobListing]) -> None:
        """Save jobs to storage."""
        raise NotImplementedError

class ExcelStorage(Storage):
    """Excel file storage handler."""
    def __init__(self, filename: str = OUTPUT_FILENAME):
        self.filename = filename

    def save(self, jobs: List[JobListing]) -> None:
        """Save jobs to Excel file."""
        df = pd.DataFrame([job.to_dict() for job in jobs])
        df.to_excel(self.filename, index=False)
        print(f"✅ Išsaugota į: {self.filename}")

class CSVStorage(Storage):
    """CSV file storage handler."""
    def __init__(self, filename: str = "uzt_adds.csv"):
        self.filename = filename

    def save(self, jobs: List[JobListing]) -> None:
        """Save jobs to CSV file."""
        df = pd.DataFrame([job.to_dict() for job in jobs])
        df.to_csv(self.filename, index=False, encoding='utf-8')
        print(f"✅ Išsaugota į: {self.filename}") 