import unittest
from unittest.mock import patch, MagicMock
from bs4 import BeautifulSoup
from .scraper import JobScraper

class TestJobScraper(unittest.TestCase):
    def setUp(self):
        self.scraper = JobScraper()

    @patch('requests.Session.get')
    def test_get_listing_links(self, mock_get):
        # Mock the response for multiple pages
        mock_responses = [
            '<div class="list"><a href="/job1">Job 1</a><a href="/job2">Job 2</a></div>',
            '<div class="list"><a href="/job3">Job 3</a><a href="/job4">Job 4</a></div>',
            '<div class="list"><a href="/job5">Job 5</a><a href="/job6">Job 6</a></div>',
            '<div class="list"><a href="/job7">Job 7</a><a href="/job8">Job 8</a></div>',
            '<div class="list"><a href="/job9">Job 9</a><a href="/job10">Job 10</a></div>'
        ]
        mock_get.side_effect = [MagicMock(text=response) for response in mock_responses]

        # Call the method
        self.scraper.get_listing_links()

        # Assertions
        self.assertEqual(len(self.scraper.jobs), 10)
        self.assertEqual(self.scraper.jobs[0].url, 'https://uzt.lt/job1')
        self.assertEqual(self.scraper.jobs[1].url, 'https://uzt.lt/job2')
        self.assertEqual(self.scraper.jobs[2].url, 'https://uzt.lt/job3')
        self.assertEqual(self.scraper.jobs[3].url, 'https://uzt.lt/job4')
        self.assertEqual(self.scraper.jobs[4].url, 'https://uzt.lt/job5')
        self.assertEqual(self.scraper.jobs[5].url, 'https://uzt.lt/job6')
        self.assertEqual(self.scraper.jobs[6].url, 'https://uzt.lt/job7')
        self.assertEqual(self.scraper.jobs[7].url, 'https://uzt.lt/job8')
        self.assertEqual(self.scraper.jobs[8].url, 'https://uzt.lt/job9')
        self.assertEqual(self.scraper.jobs[9].url, 'https://uzt.lt/job10')

if __name__ == '__main__':
    unittest.main() 