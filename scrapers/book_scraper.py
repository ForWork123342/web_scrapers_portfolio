#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Book Store Scraper with Discounts
Scrapes books with original/discounted prices
"""

import requests
from bs4 import BeautifulSoup
from utils import clean_price, save_to_csv, save_to_json

BASE_URL = 'http://books.toscrape.com/catalogue/page-{page}.html'

def scrape_books(pages: int = 5) -> list:
    books = []
    
    for page in range(1, pages + 1):
        try:
            response = requests.get(BASE_URL.format(page=page), timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            for book in soup.select('article.product_pod'):
                price = clean_price(book.select_one('p.price_color').text)
                old_price_el = book.select_one('div.product_price > p.old_price')
                old_price = clean_price(old_price_el.text) if old_price_el else None
                discount = round((old_price - price) / old_price * 100) if old_price else None
                
                books.append({
                    'title': book.h3.a['title'],
                    'current_price': price,
                    'original_price': old_price,
                    'discount_%': discount,
                    'rating': book.select_one('p.star-rating')['class'][1]
                })
                
        except Exception as e:
            print(f"⚠️ Error on page {page}: {str(e)}")
            continue
    
    return books

if __name__ == "__main__":
    print("📚 Starting book scraper with discounts...")
    books = scrape_books()
    
    if books:
        save_to_csv(books, 'books.csv')
        save_to_json(books, 'books.json')
        print(f"✅ Saved {len(books)} books with price history")