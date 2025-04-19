#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Quotes Scraper
Scrapes quotes data (без ценовой информации)
"""

import requests
from bs4 import BeautifulSoup
from utils import save_to_csv, save_to_json

BASE_URL = 'https://quotes.toscrape.com/page/{page}/'

def scrape_quotes(pages: int = 5) -> list:
    quotes = []
    
    for page in range(1, pages + 1):
        try:
            response = requests.get(BASE_URL.format(page=page), timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            for quote in soup.select('div.quote'):
                quotes.append({
                    'text': quote.select_one('span.text').text.strip(),
                    'author': quote.select_one('small.author').text.strip(),
                    'tags': [tag.text.strip() for tag in quote.select('a.tag')]
                })
                
        except Exception as e:
            print(f"⚠️ Error on page {page}: {str(e)}")
            continue
    
    return quotes

if __name__ == "__main__":
    print("💬 Starting quotes scraper...")
    quotes = scrape_quotes()
    
    if quotes:
        save_to_csv(quotes, 'quotes.csv')
        save_to_json(quotes, 'quotes.json')
        print(f"✅ Saved {len(quotes)} quotes")
    else:
        print("❌ No quotes found")