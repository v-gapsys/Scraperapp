"""
Main scraper implementation.
"""
import requests
from bs4 import BeautifulSoup
from lxml import html
import time
from typing import List, Dict
from .config import (
    BASE_URL,
    JOB_URL_PREFIX,
    MAX_JOBS,
    HEADERS,
    DELAY_BETWEEN_JOBS,
    DELAY_BETWEEN_PAGES,
    OUTPUT_FILENAME,
    REQUEST_TIMEOUT
)
from .models import JobListing
from .logger import setup_logger
import pandas as pd

class JobScraper:
    """Scraper for collecting job listings from UZT."""

    def __init__(self, base_url: str = BASE_URL, max_jobs: int = MAX_JOBS) -> None:
        """
        Initialize the JobScraper.

        Args:
            base_url (str): The base URL for the job board.
            max_jobs (int): The maximum number of jobs to scrape.
        """
        self.base_url = base_url
        self.job_url_prefix = JOB_URL_PREFIX
        self.headers = HEADERS
        self.max_jobs = max_jobs
        self.jobs: List[JobListing] = []
        self.session = requests.Session()
        self.logger = setup_logger()

    def process_job_elements(self, job_elements: List[BeautifulSoup]) -> None:
        """Process job elements and add them to the jobs list."""
        for job in job_elements:
            if len(self.jobs) >= self.max_jobs:
                self.logger.info(f"Pasiektas maksimalus skelbimų skaičius ({self.max_jobs})")
                return
            job_data = self.extract_job_summary(job)
            self.jobs.append(JobListing.from_dict(job_data))
            self.logger.info(f"Surinkta: {job_data['Pavadinimas']}")
            time.sleep(DELAY_BETWEEN_JOBS)

    def get_listing_links(self) -> None:
        """Collect exactly MAX_JOBS number of job listings."""
        start = 0
        while len(self.jobs) < self.max_jobs:
            url = f"{self.base_url}{self.job_url_prefix}" if start == 0 else f"{self.base_url}{self.job_url_prefix}/p{start}"
            self.logger.info(f"Kraunamas puslapis: {url}")
            try:
                response = self.session.get(url, headers=self.headers, timeout=REQUEST_TIMEOUT)
                response.raise_for_status()
                soup = BeautifulSoup(response.text, "html.parser")
                job_elements = soup.select("div.list > a")
                if not job_elements:
                    break
                self.process_job_elements(job_elements)
            except Exception as e:
                self.logger.error(f"Klaida: {e}")
                break
            start += 20
            time.sleep(DELAY_BETWEEN_PAGES)
        self.logger.info(f"Surinkta iš viso: {len(self.jobs)} skelbimų (tikslinis skaičius: {self.max_jobs})")

    def extract_job_summary(self, job: BeautifulSoup) -> Dict[str, str]:
        """
        Extract job summary from a job element.

        Args:
            job (BeautifulSoup): The job element to extract data from.

        Returns:
            Dict[str, str]: A dictionary containing the job summary.
        """
        title = job.select_one(".title strong")
        company = job.select_one(".company")
        location = job.select_one(".location")
        date = job.select_one(".created-date")
        salary = job.select_one(".salary")
        link = job.get("href")
        full_url = self.base_url + link
        return {
            "Pavadinimas": title.text.strip() if title else "–",
            "Įmonė": company.text.strip() if company else "–",
            "Vieta": location.text.strip() if location else "–",
            "Paskelbta": date.text.strip().replace("Įkelta: ", "") if date else "–",
            "Atlyginimas": salary.text.strip() if salary else "–",
            "Nuoroda": full_url
        }

    def enrich_job_details(self) -> None:
        """Enrich job listings with additional details."""
        for i, job in enumerate(self.jobs):
            self.logger.info(f"🔍 {i + 1}/{len(self.jobs)} Tikrinama: {job.url}")
            details = self.scrape_job_details(job.url)
            job.details.update(details)
            time.sleep(DELAY_BETWEEN_JOBS)

    def scrape_job_details(self, url: str) -> Dict[str, str]:
        """
        Scrape additional details from a job page.

        Args:
            url (str): The URL of the job page.

        Returns:
            Dict[str, str]: A dictionary containing the job details.
        """
        results = {}
        try:
            r = self.session.get(url, headers=self.headers, timeout=REQUEST_TIMEOUT)
            r.encoding = 'utf-8'
            tree = html.fromstring(r.text)
            for idx in [1, 2]:
                blocks = tree.xpath(f'//main//div[contains(@class, "meta__list")]//div[{idx}]')
                if blocks:
                    block = blocks[0]
                    sections = block.xpath('./h4')
                    for i, h4 in enumerate(sections):
                        title_el = h4.xpath('./strong/text()')
                        title = title_el[0].strip().rstrip(":") if title_el else f"Skyrius {i+1}"
                        content = []
                        next_el = h4.getnext()
                        while next_el is not None and next_el.tag != 'h4':
                            content.extend(t.strip() for t in next_el.xpath('.//text()') if t.strip())
                            next_el = next_el.getnext()
                        results[title] = '; '.join(content) if content else "–"
        except Exception as e:
            self.logger.error(f"Klaida scraping details: {e}")
            results["Klaida"] = str(e)
        return results

    def save_to_excel(self, filename: str = OUTPUT_FILENAME) -> None:
        """
        Save job listings to an Excel file.

        Args:
            filename (str): The name of the Excel file to save to.
        """
        df = pd.DataFrame(self.jobs)
        df.to_excel(filename, index=False)
        print(f"✅ Išsaugota į: {filename}") 