import unittest
from scraping.scraper import scrape_website
from processing.summarizer import summarize_text

class TestScraping(unittest.TestCase):
    def test_scrape_valid_url(self):
        url = "https://www.example.com"
        text = scrape_website(url)
        self.assertIsNotNone(text)
    
    def test_scrape_invalid_url(self):
        url = "invalid_url"
        text = scrape_website(url)
        self.assertEqual(text, "")

class TestSummarizer(unittest.TestCase):
    def test_summarize_text(self):
        text = "Your sample text here."
        summary = summarize_text(text)
        self.assertIsNotNone(summary)

if __name__ == '__main__':
    unittest.main()