"""
Storage handlers for saving scraped data.
"""
import pandas as pd
from typing import List
from .models import JobListing
from .config import OUTPUT_FILENAME

class Storage:
    """Base storage class."""
    def save(self, jobs: List[JobListing], filename: str = None) -> None:
        """Save jobs to storage."""
        raise NotImplementedError

class ExcelStorage(Storage):
    """Excel file storage handler."""
    def __init__(self, filename: str = OUTPUT_FILENAME):
        self.filename = filename

    def save(self, jobs: List[JobListing], filename: str = None) -> None:
        """Save jobs to Excel file."""
        df = pd.DataFrame([job.to_dict() for job in jobs])
        output_file = filename or self.filename
        df.to_excel(output_file, index=False)
        print(f"✅ Išsaugota į: {output_file}")

class CSVStorage(Storage):
    """CSV file storage handler."""
    def __init__(self, filename: str = "uzt_adds.csv"):
        self.filename = filename

    def save(self, jobs: List[JobListing], filename: str = None) -> None:
        """Save jobs to CSV file."""
        df = pd.DataFrame([job.to_dict() for job in jobs])
        output_file = filename or self.filename
        df.to_csv(output_file, index=False, encoding='utf-8')
        print(f"✅ Išsaugota į: {output_file}") 