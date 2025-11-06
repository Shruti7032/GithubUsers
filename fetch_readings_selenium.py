#!/usr/bin/env python3
"""
Catholic Daily Readings Fetcher using Selenium (Python equivalent to Puppeteer)

This script fetches Catholic daily readings from USCCB website using browser automation.
Based on the BambooSoftwareLLC/get-catholic-daily-readings TypeScript implementation.

Requirements:
    - selenium
    - webdriver-manager (for automatic ChromeDriver management)

Installation:
    pip install selenium webdriver-manager

Usage:
    python3 fetch_readings_selenium.py [output_path] [--format=object|array]
    
    output_path: Path to save JSON file (default: catholic_readings_2026.json)
    --format: Output format - 'object' for date-keyed or 'array' for list (default: array)
"""

import json
import sys
from datetime import date, timedelta
from typing import Dict, List, Any
import time
import re

try:
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from webdriver_manager.chrome import ChromeDriverManager
except ImportError:
    print("Error: Required packages not installed.")
    print("Install with: pip install selenium webdriver-manager")
    sys.exit(1)


class USCCBReadingsFetcher:
    """Fetches Catholic daily readings from USCCB using Selenium."""
    
    def __init__(self):
        """Initialize the fetcher with browser options."""
        self.chrome_options = Options()
        self.chrome_options.add_argument("--headless")
        self.chrome_options.add_argument("--disable-gpu")
        self.chrome_options.add_argument("--disable-dev-shm-usage")
        self.chrome_options.add_argument("--disable-setuid-sandbox")
        self.chrome_options.add_argument("--no-sandbox")
        self.chrome_options.add_argument("--no-first-run")
        self.chrome_options.add_argument("--single-process")
        self.chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        self.chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        self.chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # User agent to avoid detection
        self.chrome_options.add_argument(
            "user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36"
        )
    
    def format_date_for_url(self, target_date: date) -> str:
        """Format date as MMddyy for USCCB URL."""
        return target_date.strftime("%m%d%y")
    
    def clean_html_tags(self, text: str, preserve_newlines: bool = False) -> str:
        """Remove HTML tags and clean text."""
        if not text:
            return ""
        
        # Replace <br> with newline if preserving newlines
        if preserve_newlines:
            text = text.replace("<br>", "\n").replace("<br/>", "\n").replace("<br />", "\n")
        else:
            text = text.replace("<br>", " ").replace("<br/>", " ").replace("<br />", " ")
        
        # Remove HTML tags
        text = re.sub(r'<[^>]+>', '', text)
        
        # Clean up whitespace and nbsp
        text = text.replace("&nbsp;", " ").replace("\xa0", " ")
        text = re.sub(r'\s+', ' ', text)
        
        return text.strip()
    
    def fetch_reading_for_date(self, target_date: date) -> Dict[str, Any]:
        """Fetch reading for a specific date."""
        date_str = target_date.strftime("%Y-%m-%d")
        formatted_date = self.format_date_for_url(target_date)
        url = f"https://bible.usccb.org/bible/readings/{formatted_date}.cfm"
        
        print(f"Fetching readings for {date_str}...")
        print(f"  URL: {url}")
        
        driver = None
        try:
            # Initialize Chrome driver
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=self.chrome_options)
            driver.set_page_load_timeout(30)
            
            # Load the page
            driver.get(url)
            
            # Wait for the lectionary section to load
            wait = WebDriverWait(driver, 10)
            lectionary_element = wait.until(
                EC.presence_of_element_located((By.CLASS_NAME, "b-lectionary"))
            )
            
            # Extract header (e.g., "Monday of the Thirty-first Week in Ordinary Time")
            try:
                header_element = lectionary_element.find_element(By.CSS_SELECTOR, "div.innerblock h2")
                header = header_element.text.strip()
            except:
                header = f"Daily Reading - {target_date.strftime('%A')}"
            
            # Extract lectionary number
            lectionary_number = ""
            try:
                lectionary_text_element = lectionary_element.find_element(By.CSS_SELECTOR, "div.innerblock p")
                lectionary_text = lectionary_text_element.text.strip()
                match = re.search(r'\d+', lectionary_text)
                if match:
                    lectionary_number = match.group(0)
            except:
                pass
            
            # Find all reading blocks
            reading_elements = driver.find_elements(By.CLASS_NAME, "b-verse")
            
            readings = []
            for reading_elem in reading_elements:
                try:
                    # Extract reading type (e.g., "Reading 1", "Responsorial Psalm", "Gospel")
                    reading_type = ""
                    try:
                        type_element = reading_elem.find_element(By.CSS_SELECTOR, "div.content-header h3.name")
                        reading_type = type_element.text.strip()
                    except:
                        pass
                    
                    # Extract reference (e.g., "Lk 2:16-21")
                    reference = ""
                    try:
                        ref_element = reading_elem.find_element(By.CSS_SELECTOR, "div.address a")
                        reference = ref_element.text.strip()
                    except:
                        pass
                    
                    # Extract reading text
                    text = ""
                    try:
                        content_element = reading_elem.find_element(By.CSS_SELECTOR, "div.content-body")
                        raw_html = content_element.get_attribute('innerHTML')
                        text = self.clean_html_tags(raw_html, preserve_newlines=False)
                    except:
                        pass
                    
                    if reading_type and text:
                        readings.append({
                            "type": reading_type,
                            "citation": reference,
                            "text": text
                        })
                
                except Exception as e:
                    print(f"  ⚠ Error parsing reading block: {e}")
                    continue
            
            if readings:
                print(f"  ✓ Successfully fetched {len(readings)} readings")
                return {
                    "date": date_str,
                    "title": header,
                    "lectionary": lectionary_number,
                    "readings": readings
                }
            else:
                print(f"  ⚠ No readings found")
                return self.create_placeholder(date_str, header)
        
        except Exception as e:
            print(f"  ✗ Error: {e}")
            return self.create_placeholder(date_str)
        
        finally:
            if driver:
                driver.quit()
    
    def create_placeholder(self, date_str: str, title: str = None) -> Dict[str, Any]:
        """Create placeholder reading entry."""
        target_date = date.fromisoformat(date_str)
        default_title = title or f"Daily Reading - {target_date.strftime('%A')}"
        
        return {
            "date": date_str,
            "title": default_title,
            "lectionary": "",
            "readings": [
                {
                    "type": "First Reading",
                    "citation": "Data not yet available",
                    "text": f"Reading data for {date_str} will be available when published by USCCB."
                },
                {
                    "type": "Psalm",
                    "citation": "Data not yet available",
                    "text": f"Psalm for {date_str} will be available when published."
                },
                {
                    "type": "Gospel",
                    "citation": "Data not yet available",
                    "text": f"Gospel reading for {date_str} will be available when published."
                }
            ]
        }
    
    def fetch_all_readings(self, start_date: date, end_date: date, output_path: str = None, format_type: str = 'array') -> List[Dict[str, Any]]:
        """
        Fetch readings for all days in the date range, saving incrementally.
        
        Args:
            start_date: Start date
            end_date: End date
            output_path: Path to save JSON file
            format_type: 'array' (default) or 'object' for date-keyed format
        """
        total_days = (end_date - start_date).days + 1
        readings = []
        
        print("=" * 70)
        print("Catholic Daily Readings Fetcher (Python/Selenium)")
        print("Fetching from USCCB website")
        print("=" * 70)
        print()
        print(f"Date range: {start_date} to {end_date}")
        print(f"Total days: {total_days}")
        if output_path:
            print(f"Saving incrementally to: {output_path}")
            print(f"Output format: {format_type}")
        print()
        
        current_date = start_date
        day_count = 0
        
        while current_date <= end_date:
            day_count += 1
            
            if day_count % 10 == 0 or day_count == 1:
                print(f"Progress: {day_count}/{total_days} days processed")
            
            reading = self.fetch_reading_for_date(current_date)
            readings.append(reading)
            
            # Save incrementally after each date
            if output_path:
                self.save_to_json(readings, output_path, format_type=format_type)
                print(f"  ✓ Saved to {output_path} ({len(readings)} entries)")
            
            # Add delay between requests to be respectful
            time.sleep(2)
            
            current_date += timedelta(days=1)
        
        print()
        print(f"Completed! Fetched {len(readings)} daily readings.")
        return readings
    
    def save_to_json(self, readings: List[Dict[str, Any]], output_path: str, 
                     show_details: bool = False, format_type: str = 'array') -> None:
        """
        Save readings to JSON file.
        
        Args:
            readings: List of reading dictionaries
            output_path: Path to save the file
            show_details: Whether to print file details
            format_type: 'array' (default) or 'object' (date-keyed)
        """
        # Convert to object format if requested
        if format_type == 'object':
            data = self._convert_to_object_format(readings)
        else:
            data = readings
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        if show_details:
            print(f"\nJSON file saved to: {output_path}")
            file_size = len(json.dumps(data))
            print(f"File size: {file_size:,} bytes ({file_size/1024:.1f} KB)")
            print(f"Format: {format_type}")
    
    def _convert_to_object_format(self, readings: List[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
        """
        Convert array format to object format.
        
        Input:  [{"date": "2025-11-01", "title": "...", ...}, ...]
        Output: {"2025-11-01": {"title": "...", ...}, ...}
        """
        result = {}
        for reading in readings:
            if 'date' in reading:
                date_key = reading['date']
                # Create new object without the date field
                reading_obj = {k: v for k, v in reading.items() if k != 'date'}
                result[date_key] = reading_obj
        return result


def main():
    """Main entry point."""
    print("=" * 70)
    print("Catholic Daily Readings Fetcher")
    print("Using Selenium to scrape USCCB website")
    print("=" * 70)
    print()
    print("COPYRIGHT NOTICE:")
    print("-" * 70)
    print("This script fetches readings from USCCB website for personal use.")
    print("Please review USCCB's terms of service for redistribution rights.")
    print("Consider using MIT-licensed APIs for commercial applications.")
    print("=" * 70)
    print()
    
    # Parse command-line arguments
    output_path = "catholic_readings_2026.json"
    format_type = 'array'  # default to array format
    
    for arg in sys.argv[1:]:
        if arg.startswith('--format='):
            format_type = arg.split('=')[1].lower()
            if format_type not in ['array', 'object']:
                print(f"Error: Invalid format '{format_type}'. Must be 'array' or 'object'")
                sys.exit(1)
        elif not arg.startswith('--'):
            output_path = arg
    
    print(f"Output file: {output_path}")
    print(f"Output format: {format_type}")
    if format_type == 'object':
        print("  (Date-keyed object for direct lookup)")
    else:
        print("  (Array of reading objects)")
    print(f"Note: File will be saved incrementally after each date is fetched.")
    print()
    
    # Date range: Nov 2025 to Dec 2026
    start_date = date(2025, 11, 1)
    end_date = date(2026, 12, 31)
    
    # Fetch readings with incremental saving
    fetcher = USCCBReadingsFetcher()
    readings = fetcher.fetch_all_readings(start_date, end_date, output_path, format_type)
    
    # Final save with details
    fetcher.save_to_json(readings, output_path, show_details=True, format_type=format_type)
    
    # Summary
    actual_readings = sum(1 for r in readings 
                         if 'will be available' not in r['readings'][0]['text'])
    
    print()
    print("=" * 70)
    print("SUMMARY:")
    print("-" * 70)
    print(f"Total entries: {len(readings)}")
    print(f"Entries with actual readings: {actual_readings}")
    print(f"Entries with placeholders: {len(readings) - actual_readings}")
    print(f"Date range: {readings[0]['date']} to {readings[-1]['date']}")
    print()
    print("✓ File ready for Android app!")
    print("=" * 70)


if __name__ == "__main__":
    main()
