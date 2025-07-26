# BBC News Scraper with Selenium & BeautifulSoup

A Python web scraper that collects news article titles and links from the [BBC News](https://www.bbc.com/news) website using **Selenium** and **BeautifulSoup**, and saves them into a CSV file.

## Features

- Launches a headless browser to load BBC News
- Waits for the main page content to be fully loaded
- Scrolls to the bottom to trigger lazy-loaded content
- Parses dynamic HTML using BeautifulSoup
- Extracts article titles and valid news links
- Saves articles to `bbc_articles.csv`
- Automatically captures screenshots and debug HTML if scraping fails

### Requirements

- Python 3.7 or above
- Google Chrome
- ChromeDriver (must match your Chrome version)

#### Python Packages

Install the required packages:
pip install selenium beautifulsoup4
