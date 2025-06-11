#!/usr/bin/env python3
"""
Main script for running the UZT job scraper.
"""

from scraper.scraper import JobScraper
from scraper.config import MAX_JOBS, REFERENCE_JOB
from scraper.storage import ExcelStorage, CSVStorage
from scraper.analysis import SalaryAnalyzer
from scraper.similarity import compute_similarity
from scraper.logger import setup_logger
import json
import os
import csv
import sys

def main():
    """Main function to run the scraper."""
    # Set up logger
    logger = setup_logger()
    
    # Create output directory if it doesn't exist
    os.makedirs('output', exist_ok=True)
    
    # Initialize scraper
    scraper = JobScraper()
    
    # Scrape jobs
    scraper.get_listing_links()
    scraper.enrich_job_details()
    
    # Save to Excel and CSV in output folder
    excel_path = os.path.join('output', 'uzt_adds.xlsx')
    csv_path = os.path.join('output', 'uzt_adds.csv')
    excel_storage = ExcelStorage()
    csv_storage = CSVStorage()
    
    excel_storage.save(scraper.jobs, excel_path)
    csv_storage.save(scraper.jobs, csv_path)
    
    # Perform salary analysis
    analyzer = SalaryAnalyzer(scraper.jobs)
    stats = analyzer.get_statistics()
    
    # Print salary statistics
    sys.stdout.write("\nSalary Statistics:\n")
    sys.stdout.flush()
    logger.info("\nSalary Statistics:")
    
    sys.stdout.write(f"Total jobs analyzed: {stats.total_jobs}\n")
    sys.stdout.flush()
    logger.info(f"Total jobs analyzed: {stats.total_jobs}")
    
    sys.stdout.write(f"Jobs with valid salary: {stats.valid_salaries_count}\n")
    sys.stdout.flush()
    logger.info(f"Jobs with valid salary: {stats.valid_salaries_count}")
    
    sys.stdout.write(f"Mean salary: €{stats.mean:.2f}\n")
    sys.stdout.flush()
    logger.info(f"Mean salary: €{stats.mean:.2f}")
    
    sys.stdout.write(f"Median salary: €{stats.median:.2f}\n")
    sys.stdout.flush()
    logger.info(f"Median salary: €{stats.median:.2f}")
    
    sys.stdout.write(f"Standard deviation: €{stats.std:.2f}\n")
    sys.stdout.flush()
    logger.info(f"Standard deviation: €{stats.std:.2f}")
    
    sys.stdout.write(f"Salary range: €{stats.min:.2f} - €{stats.max:.2f}\n")
    sys.stdout.flush()
    logger.info(f"Salary range: €{stats.min:.2f} - €{stats.max:.2f}")
    
    sys.stdout.write(f"Quartiles: €{stats.quartiles[0]:.2f}, €{stats.quartiles[1]:.2f}, €{stats.quartiles[2]:.2f}\n")
    sys.stdout.flush()
    logger.info(f"Quartiles: €{stats.quartiles[0]:.2f}, €{stats.quartiles[1]:.2f}, €{stats.quartiles[2]:.2f}")
    
    # Get and print salary by location
    location_salaries = analyzer.get_salary_by_location()
    sys.stdout.write("\nAverage Salary by Location:\n")
    sys.stdout.flush()
    logger.info("\nAverage Salary by Location:")
    
    for location, salary in location_salaries.items():
        sys.stdout.write(f"{location}: €{salary:.2f}\n")
        sys.stdout.flush()
        logger.info(f"{location}: €{salary:.2f}")
    
    # Save analysis results
    analysis_path = os.path.join('output', 'salary_analysis.json')
    analysis_results = {
        'statistics': {
            'mean': float(stats.mean),
            'median': float(stats.median),
            'std': float(stats.std),
            'min': float(stats.min),
            'max': float(stats.max),
            'quartiles': stats.quartiles.tolist(),
            'valid_salaries_count': stats.valid_salaries_count,
            'total_jobs': stats.total_jobs
        },
        'location_salaries': {
            location: float(salary)
            for location, salary in location_salaries.items()
        }
    }
    
    with open(analysis_path, 'w', encoding='utf-8') as f:
        json.dump(analysis_results, f, ensure_ascii=False, indent=2)
    sys.stdout.write(f"\n✅ Analysis results saved to: {analysis_path}\n")
    sys.stdout.flush()
    logger.info(f"\n✅ Analysis results saved to: {analysis_path}")

    # Compute similarity
    similarity_results = compute_similarity(REFERENCE_JOB, scraper.jobs)
    sys.stdout.write("\nJob Offers Listed by Similarity:\n")
    sys.stdout.flush()
    logger.info("\nJob Offers Listed by Similarity:")
    
    for job, similarity in similarity_results:
        sys.stdout.write(f"Job: {job.title} - Similarity: {similarity:.4f}\n")
        sys.stdout.flush()
        logger.info(f"Job: {job.title} - Similarity: {similarity:.4f}")

    # Save similarity rankings to CSV
    similarity_csv_path = os.path.join('output', 'similarity_rankings.csv')
    with open(similarity_csv_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Title', 'Location', 'Salary', 'Similarity'])
        for job, score in similarity_results:
            writer.writerow([
                getattr(job, 'title', ''),
                getattr(job, 'location', ''),
                getattr(job, 'salary', ''),
                f"{score:.4f}"
            ])
    sys.stdout.write(f"\n✅ Similarity rankings saved to: {similarity_csv_path}\n\n")
    sys.stdout.flush()
    logger.info(f"\n✅ Similarity rankings saved to: {similarity_csv_path}\n")

if __name__ == "__main__":
    main() 