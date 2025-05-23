"""
Configuration settings for the scraper.
"""

# Scraping Configuration

# Base URL for the job board
BASE_URL = "https://uzt.lt"

# Job listing URL prefix
JOB_URL_PREFIX = "/laisvos-darbo-vietos/436/results"

# Maximum number of jobs to scrape
MAX_JOBS = 42

# Request headers
HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept-Language": "lt-LT,lt;q=0.9,en-US;q=0.8,en;q=0.7"
}

# Delay settings (in seconds)
DELAY_BETWEEN_JOBS = 1  # Delay between scraping individual jobs
DELAY_BETWEEN_PAGES = 2  # Delay between scraping pages
RANDOM_DELAY = True  # Add random delay to avoid detection
MIN_RANDOM_DELAY = 0.5  # Minimum random delay in seconds
MAX_RANDOM_DELAY = 2.0  # Maximum random delay in seconds

# Request settings
REQUEST_TIMEOUT = 10  # Request timeout in seconds
MAX_RETRIES = 3  # Maximum number of retries for failed requests
RETRY_DELAY = 5  # Delay between retries in seconds

# Proxy settings (optional)
USE_PROXY = False
PROXIES = {
    "http": None,
    "https": None
}

# Output file settings
OUTPUT_FILENAME = "uzt_adds.xlsx"

# Request timeout (in seconds)
REQUEST_TIMEOUT = 10 