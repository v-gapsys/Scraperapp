# UZT Job Scraper

A Python-based web scraper for collecting job listings from UZT.lt. This scraper is designed to gather job information and save it in both Excel and CSV formats.

## Project Structure

```
Scraperapp/
├── src/                    # Source code directory
│   ├── scraper/           # Scraper package
│   │   ├── __init__.py    # Package initialization
│   │   ├── config.py      # Configuration settings
│   │   ├── models.py      # Data models
│   │   ├── scraper.py     # Main scraper implementation
│   │   ├── storage.py     # Storage handlers
│   │   └── logger.py      # Logging configuration
│   └── main.py            # Main script to run the scraper
├── output/                # Output directory for scraped data
├── logs/                  # Log files directory
├── requirements.txt       # Project dependencies
└── README.md             # Project documentation
```

## Features

- Scrapes job listings from UZT.lt
- Extracts detailed job information
- Saves data in both Excel and CSV formats
- Configurable scraping parameters
- Comprehensive logging
- Error handling and retry mechanism
- Random delays to avoid detection

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd Scraperapp
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Configuration

The scraper's behavior can be configured in `src/scraper/config.py`. Key settings include:

- `MAX_JOBS`: Maximum number of jobs to scrape (default: 10)
- `DELAY_BETWEEN_JOBS`: Delay between scraping individual jobs
- `DELAY_BETWEEN_PAGES`: Delay between scraping pages
- `OUTPUT_FILENAME`: Base name for output files
- `REQUEST_TIMEOUT`: Timeout for HTTP requests

## Usage

1. Ensure you're in the virtual environment:
```bash
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Run the scraper:
```bash
python src/main.py
```

The scraper will:
- Collect job listings from UZT.lt
- Extract detailed information for each job
- Save the results in both Excel and CSV formats in the `output` directory
- Create log files in the `logs` directory

## Output

The scraper generates two types of output files in the `output` directory:
- `uzt_adds.xlsx`: Excel file with job listings
- `uzt_adds.csv`: CSV file with job listings

## Logging

Log files are stored in the `logs` directory with timestamps in their names. The logs include:
- Scraping progress
- Job collection details
- Any errors or warnings
- Completion status

## Dependencies

- Python 3.8+
- requests
- beautifulsoup4
- lxml
- pandas
- openpyxl

## License

This project is licensed under the MIT License - see the LICENSE file for details. 