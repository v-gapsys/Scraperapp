"""
Data models for the scraper.
"""
from dataclasses import dataclass
from typing import Dict

@dataclass
class JobListing:
    """Represents a job listing with all its details."""
    title: str
    company: str
    location: str
    posted_date: str
    salary: str
    url: str
    details: Dict[str, str]

    @classmethod
    def from_dict(cls, data: dict) -> 'JobListing':
        """Create a JobListing instance from a dictionary."""
        return cls(
            title=data.get('Pavadinimas', '–'),
            company=data.get('Įmonė', '–'),
            location=data.get('Vieta', '–'),
            posted_date=data.get('Paskelbta', '–'),
            salary=data.get('Atlyginimas', '–'),
            url=data.get('Nuoroda', ''),
            details={k: v for k, v in data.items() if k not in ['Pavadinimas', 'Įmonė', 'Vieta', 'Paskelbta', 'Atlyginimas', 'Nuoroda']}
        )

    def to_dict(self) -> dict:
        """Convert the JobListing to a dictionary."""
        return {
            'Pavadinimas': self.title,
            'Įmonė': self.company,
            'Vieta': self.location,
            'Paskelbta': self.posted_date,
            'Atlyginimas': self.salary,
            'Nuoroda': self.url,
            **self.details
        } 