#!/usr/bin/env python3
"""
Main script for running the UZT job scraper.
"""

from scraper.scraper import JobScraper
from scraper.config import MAX_JOBS
from scraper.storage import ExcelStorage, CSVStorage
from scraper.analysis import SalaryAnalyzer
import json

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
    
    # Perform salary analysis
    analyzer = SalaryAnalyzer(scraper.jobs)
    stats = analyzer.get_statistics()
    
    # Print salary statistics
    print("\nSalary Statistics:")
    print(f"Total jobs analyzed: {stats.total_jobs}")
    print(f"Jobs with valid salary: {stats.valid_salaries_count}")
    print(f"Mean salary: €{stats.mean:.2f}")
    print(f"Median salary: €{stats.median:.2f}")
    print(f"Standard deviation: €{stats.std:.2f}")
    print(f"Salary range: €{stats.min:.2f} - €{stats.max:.2f}")
    print(f"Quartiles: €{stats.quartiles[0]:.2f}, €{stats.quartiles[1]:.2f}, €{stats.quartiles[2]:.2f}")
    
    # Get and print salary by location
    location_salaries = analyzer.get_salary_by_location()
    print("\nAverage Salary by Location:")
    for location, salary in location_salaries.items():
        print(f"{location}: €{salary:.2f}")
    
    # Save analysis results to JSON
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
    
    with open('output/salary_analysis.json', 'w', encoding='utf-8') as f:
        json.dump(analysis_results, f, indent=2, ensure_ascii=False)
    print("\n✅ Analysis results saved to: output/salary_analysis.json")

if __name__ == "__main__":
    main() 