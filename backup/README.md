# UZT Job Scraper

A Python-based web scraper for collecting job listings from uzt.lt. The scraper collects job information including titles, companies, locations, dates, salaries, and detailed job descriptions.

## Features

- Scrapes job listings from uzt.lt
- Collects basic job information (title, company, location, date, salary)
- Enriches job data with detailed descriptions
- Saves results to Excel file
- Configurable number of jobs to scrape
- Rate limiting to prevent server overload

## Setup

1. Create and activate a virtual environment:
   ```bash
   # On macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   
   # On Windows
   python -m venv venv
   .\venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Simply run the script:
```bash
python Scraperapp.py
```

The script will:
1. Scrape job listings from uzt.lt
2. Collect detailed information for each job
3. Save the results to `uzt_adds.xlsx`

## Configuration

You can modify the following parameters in the code:
- `max_jobs`: Maximum number of jobs to scrape (default: 40)
- `base_url`: Base URL of the website (default: "https://uzt.lt")

## Output

The script generates an Excel file (`uzt_adds.xlsx`) containing the following information for each job:
- Pavadinimas (Title)
- Įmonė (Company)
- Vieta (Location)
- Paskelbta (Posted Date)
- Atlyginimas (Salary)
- Nuoroda (URL)
- Additional job details from the detailed view

## Note

Please be mindful of the website's terms of service and implement appropriate delays between requests to avoid overloading the server. 