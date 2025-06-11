# UZT Job Scraper

A Python-based web scraper for collecting job listings from UZT.lt. This scraper is designed to gather job information and save it in both Excel and CSV formats, with advanced salary and similarity analysis.

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
│   │   ├── analysis.py    # Data analysis tools
│   │   ├── similarity.py  # Similarity analysis
│   │   └── logger.py      # Logging configuration
│   └── main.py            # Main script to run the scraper
├── test/                  # Test directory
│   ├── __init__.py        # Test package initialization
│   └── test_scraper.py    # Test cases for the scraper
├── output/                # Output directory for scraped data
├── logs/                  # Log files directory
├── requirements.txt       # Project dependencies
└── README.md             # Project documentation
```

## Features

- Scrapes job listings from UZT.lt
- Extracts detailed job information
- Saves data in both Excel and CSV formats (in the `output` directory)
- Configurable scraping parameters
- Comprehensive logging (to both console and log files)
- Error handling and retry mechanism
- Random delays to avoid detection
- Advanced salary analysis using NumPy
  - Statistical analysis (mean, median, standard deviation)
  - Salary distribution analysis
  - Location-based salary analysis
  - Salary range and quartile calculations
- Similarity analysis using TF-IDF and cosine similarity
  - Ranks job offers by similarity to a reference job
  - Results saved to `output/similarity_rankings.csv`

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd Scraperapp
```

2. Create and activate a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Configuration

The scraper's behavior can be configured in `src/scraper/config.py`. Key settings include:

- `MAX_JOBS`: Maximum number of jobs to scrape (default: 15)
- `DELAY_BETWEEN_JOBS`: Delay between scraping individual jobs
- `DELAY_BETWEEN_PAGES`: Delay between scraping pages
- `OUTPUT_FILENAME`: Base name for output files
- `REQUEST_TIMEOUT`: Timeout for HTTP requests
- `REFERENCE_JOB`: Reference job for similarity analysis

## Usage

1. Ensure you're in the virtual environment:
```bash
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Run the scraper:
```bash
python3 src/main.py
```

The scraper will:
- Collect job listings from UZT.lt
- Extract detailed information for each job
- Save the results in both Excel and CSV formats in the `output` directory
- Create log files in the `logs` directory
- Print progress and results to the console as well as to log files
- Perform salary analysis and save results to `output/salary_analysis.json` and `output/salary_analysis.csv`
- Perform similarity analysis and save rankings to `output/similarity_rankings.csv`

## Output

The scraper generates several output files in the `output` directory:
- `uzt_adds.xlsx`: Excel file with job listings
- `uzt_adds.csv`: CSV file with job listings
- `salary_analysis.json`: Detailed salary analysis including:
  - Overall statistics (mean, median, standard deviation)
  - Salary ranges and quartiles
  - Location-based salary averages
  - Distribution data
- `salary_analysis.csv`: Salary analysis in CSV format
- `similarity_rankings.csv`: Job offers ranked by similarity to the reference job

## Salary & Similarity Analysis

The scraper includes advanced analysis capabilities:

1. **Statistical Analysis:**
   - Mean and median salary calculations
   - Standard deviation
   - Minimum and maximum salaries
   - Quartile analysis

2. **Location-based Analysis:**
   - Average salaries by city/location
   - Regional salary comparisons

3. **Distribution Analysis:**
   - Salary distribution across different ranges
   - Histogram data for visualization

4. **Similarity Analysis:**
   - Uses TF-IDF vectorization and cosine similarity (via scikit-learn)
   - Ranks all job offers by similarity to the reference job defined in `config.py`
   - Results are printed to the console and saved to `output/similarity_rankings.csv`

## Logging & Console Output

- All progress, statistics, and results are printed to the console and also logged to files in the `logs` directory.
- Log files are timestamped and include scraping progress, job collection details, errors/warnings, and completion status.

## Dependencies

- Python 3.8+
- requests
- beautifulsoup4
- lxml
- pandas
- openpyxl
- numpy
- scikit-learn

## Testing

To run the tests:

```bash
python3 -m unittest test/test_scraper.py -v
```

The test suite includes:
- Unit tests for the scraper functionality
- Mocked HTTP responses to avoid actual web requests during testing
- Verification of job listing collection and processing

## Troubleshooting

- **No module named 'sklearn'**: Make sure you have activated your virtual environment and installed all dependencies with `pip install -r requirements.txt`.
- **No printing to console**: The application prints and logs output. If you don't see console output, check your terminal settings or try running with `python3` instead of `python`.
- **Permission errors**: Ensure you have write permissions to the `output` and `logs` directories.
- **Python version**: Use `python3` for all commands to avoid version mismatches.

## License

This project is licensed under the MIT License - see the LICENSE file for details. 