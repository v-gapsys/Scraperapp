import requests
from bs4 import BeautifulSoup
from lxml import html
import pandas as pd
import time

class JobScraper:
    def __init__(self, base_url="https://uzt.lt", max_jobs=40):
        self.base_url = base_url
        self.job_url_prefix = "/laisvos-darbo-vietos/436/results"
        self.headers = {
            "User-Agent": "Mozilla/5.0",
            "Accept-Language": "lt-LT,lt;q=0.9,en-US;q=0.8,en;q=0.7"
        }
        self.max_jobs = max_jobs
        self.jobs = []
        self.session = requests.Session()

    def get_listing_links(self):
        start = 0
        while len(self.jobs) < self.max_jobs:
            url = f"{self.base_url}{self.job_url_prefix}" if start == 0 else f"{self.base_url}{self.job_url_prefix}/p{start}"
            print(f"Kraunamas puslapis: {url}")
            try:
                response = self.session.get(url, headers=self.headers, timeout=10)
                response.raise_for_status()
                soup = BeautifulSoup(response.text, "html.parser")
                job_elements = soup.select("div.list > a")
                if not job_elements:
                    break
                for job in job_elements:
                    if len(self.jobs) >= self.max_jobs:
                        break
                    job_data = self.extract_job_summary(job)
                    self.jobs.append(job_data)
                    print(f"Surinkta: {job_data['Pavadinimas']}")
                    time.sleep(1)
            except Exception as e:
                print(f"Klaida: {e}")
                break
            start += 20
            time.sleep(2)

    def extract_job_summary(self, job):
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

    def enrich_job_details(self):
        for i, job in enumerate(self.jobs):
            print(f"🔍 {i + 1}/{len(self.jobs)} Tikrinama: {job['Nuoroda']}")
            details = self.scrape_job_details(job["Nuoroda"])
            job.update(details)
            time.sleep(2)

    def scrape_job_details(self, url):
        results = {}
        try:
            r = self.session.get(url, headers=self.headers, timeout=10)
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
            results["Klaida"] = str(e)
        return results

    def save_to_excel(self, filename="uzt_adds.xlsx"):
        df = pd.DataFrame(self.jobs)
        df.to_excel(filename, index=False)
        print(f"✅ Išsaugota į: {filename}")

if __name__ == "__main__":
    scraper = JobScraper(max_jobs=40)
    scraper.get_listing_links()
    scraper.enrich_job_details()
    scraper.save_to_excel() 