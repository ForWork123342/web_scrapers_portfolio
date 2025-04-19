#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Utility functions for all scrapers
"""

import pandas as pd
import csv
import json
from typing import List, Dict
from openpyxl.utils import get_column_letter

def clean_price(price_text: str) -> float:
    """Extracts numeric price from text"""
    if not price_text:
        return None
    return float(''.join(c for c in price_text if c.isdigit() or c == '.'))

def save_to_csv(data: List[Dict], filename: str) -> None:
    """Saves data to CSV with UTF-8 encoding"""
    with open(filename, 'w', encoding='utf-8', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)

def save_to_json(data: List[Dict], filename: str, indent: int = 4) -> None:
    """Saves data to JSON file with pretty-print"""
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=indent)

def save_to_excel(data: pd.DataFrame, filename: str) -> None:
    """Saves DataFrame to Excel with auto-width columns"""
    with pd.ExcelWriter(filename) as writer:
        data.to_excel(writer, index=False)
        worksheet = writer.sheets['Sheet1']
        
        for idx, col in enumerate(data.columns):
            max_len = max(
                data[col].astype(str).map(len).max(),
                len(str(col))
            ) + 2
            worksheet.column_dimensions[get_column_letter(idx+1)].width = min(max_len, 50)