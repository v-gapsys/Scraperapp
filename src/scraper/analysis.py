"""
Analysis module for processing and analyzing job data.
"""
import numpy as np
from typing import List, Dict, Optional
from .models import JobListing
import re
from dataclasses import dataclass

@dataclass
class SalaryStats:
    """Data class for storing salary statistics."""
    mean: float
    median: float
    std: float
    min: float
    max: float
    quartiles: np.ndarray
    valid_salaries_count: int
    total_jobs: int

class SalaryAnalyzer:
    """Class for analyzing salary data from job listings."""
    
    def __init__(self, jobs: List[JobListing]):
        """
        Initialize the SalaryAnalyzer with a list of job listings.
        
        Args:
            jobs (List[JobListing]): List of job listings to analyze
        """
        self.jobs = jobs
        self._salary_array: Optional[np.ndarray] = None
    
    def _parse_salary(self, salary_str: str) -> Optional[float]:
        """
        Parse salary string into a numeric value.
        
        Args:
            salary_str (str): Salary string to parse
            
        Returns:
            Optional[float]: Parsed salary value or None if invalid
        """
        if not salary_str or salary_str == '–':
            return None
            
        # Remove currency symbols, whitespace, and "per mėn."
        salary_str = salary_str.strip().replace('€', '').replace(' ', '').replace('/permėn.', '')
        
        # Try to extract numeric value
        try:
            # Handle ranges (e.g., "1000-2000")
            if '-' in salary_str:
                min_salary, max_salary = map(float, salary_str.split('-'))
                return (min_salary + max_salary) / 2
            # Handle single values
            return float(salary_str)
        except (ValueError, TypeError):
            return None
    
    def _prepare_salary_data(self) -> np.ndarray:
        """
        Prepare salary data for analysis.
        
        Returns:
            np.ndarray: Array of valid salary values
        """
        if self._salary_array is None:
            # Parse all salaries and filter out None values
            salaries = [self._parse_salary(job.salary) for job in self.jobs]
            self._salary_array = np.array([s for s in salaries if s is not None])
        return self._salary_array
    
    def get_statistics(self) -> SalaryStats:
        """
        Calculate salary statistics.
        
        Returns:
            SalaryStats: Object containing salary statistics
        """
        salaries = self._prepare_salary_data()
        
        if len(salaries) == 0:
            return SalaryStats(
                mean=0.0,
                median=0.0,
                std=0.0,
                min=0.0,
                max=0.0,
                quartiles=np.array([0.0, 0.0, 0.0]),
                valid_salaries_count=0,
                total_jobs=len(self.jobs)
            )
        
        return SalaryStats(
            mean=np.mean(salaries),
            median=np.median(salaries),
            std=np.std(salaries),
            min=np.min(salaries),
            max=np.max(salaries),
            quartiles=np.percentile(salaries, [25, 50, 75]),
            valid_salaries_count=len(salaries),
            total_jobs=len(self.jobs)
        )
    
    def get_salary_distribution(self, bins: int = 10) -> Dict[str, np.ndarray]:
        """
        Calculate salary distribution.
        
        Args:
            bins (int): Number of bins for the histogram
            
        Returns:
            Dict[str, np.ndarray]: Dictionary containing histogram data
        """
        salaries = self._prepare_salary_data()
        
        if len(salaries) == 0:
            return {
                'histogram': np.array([]),
                'bin_edges': np.array([])
            }
        
        histogram, bin_edges = np.histogram(salaries, bins=bins)
        return {
            'histogram': histogram,
            'bin_edges': bin_edges
        }
    
    def get_salary_by_location(self) -> Dict[str, float]:
        """
        Calculate average salary by location.
        
        Returns:
            Dict[str, float]: Dictionary mapping locations to average salaries
        """
        location_salaries = {}
        
        for job in self.jobs:
            salary = self._parse_salary(job.salary)
            if salary is not None:
                if job.location not in location_salaries:
                    location_salaries[job.location] = []
                location_salaries[job.location].append(salary)
        
        return {
            location: np.mean(salaries)
            for location, salaries in location_salaries.items()
            if len(salaries) > 0
        } 