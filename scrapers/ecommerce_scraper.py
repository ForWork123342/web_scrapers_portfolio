#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
E-commerce Scraper with Discount Support
Scrapes products with regular/discount prices
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
from utils import clean_price, save_to_excel

BASE_URL = 'https://www.scrapingcourse.com/ecommerce/page/{page}/'

def scrape_products(pages: int = 3) -> pd.DataFrame:
    products = []
    
    for page in range(1, pages + 1):
        try:
            response = requests.get(BASE_URL.format(page=page), timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            for product in soup.select('li.product'):
                # Акционная цена
                current_price_el = product.select_one('ins .woocommerce-Price-amount') or \
                                 product.select_one('.price .woocommerce-Price-amount')
                # Старая цена (если есть скидка)
                old_price_el = product.select_one('del .woocommerce-Price-amount')
                
                current_price = clean_price(current_price_el.text if current_price_el else None)
                old_price = clean_price(old_price_el.text if old_price_el else None)
                discount = round((old_price - current_price) / old_price * 100) if old_price else None
                
                products.append({
                    'name': product.find('h2').get_text(strip=True),
                    'current_price': current_price,
                    'old_price': old_price,
                    'discount_%': discount,
                    'image': product.find('img')['src'] if product.find('img') else None
                })
                
        except Exception as e:
            print(f"⚠️ Error on page {page}: {str(e)}")
            continue
    
    return pd.DataFrame(products)

if __name__ == "__main__":
    print("🛍️ Starting e-commerce scraper with discount support...")
    df = scrape_products()
    
    if not df.empty:
        save_to_excel(df, 'ecommerce_products.xlsx')
        print(f"✅ Saved {len(df)} products with discount info")