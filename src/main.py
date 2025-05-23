#!/usr/bin/env python3
"""
Main script for running the UZT job scraper.
"""

from scraper.scraper import JobScraper
from scraper.config import MAX_JOBS
from scraper.storage import ExcelStorage, CSVStorage

def main():
    """Main function to run the scraper."""
    # Print MAX_JOBS value for debugging
    print(f"[DEBUG] MAX_JOBS from config: {MAX_JOBS}")
    # Initialize scraper
    scraper = JobScraper()
    
    # Scrape jobs
    scraper.get_listing_links()
    scraper.enrich_job_details()
    
    # Save to both Excel and CSV
    excel_storage = ExcelStorage()
    csv_storage = CSVStorage()
    
    excel_storage.save(scraper.jobs)
    csv_storage.save(scraper.jobs)

if __name__ == "__main__":
    main() 