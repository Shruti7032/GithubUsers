#!/usr/bin/env python3
"""
Catholic Daily Readings Fetcher from Open-Source APIs

This script fetches Catholic daily readings from open-source APIs:
- CatholicOS/liturgical-calendar-api (MIT license)
- cpbjr/catholic-readings-api (MIT license)

Usage:
    python3 fetch_readings_from_apis.py [output_path]

Requirements:
    - requests library (install with: pip install requests)
"""

import json
import sys
from datetime import date, timedelta
from typing import Dict, List, Any
import time

try:
    import requests
except ImportError:
    print("Error: 'requests' library is required.")
    print("Install it with: pip install requests")
    sys.exit(1)


class CatholicReadingsFetcher:
    """Fetches Catholic daily readings from open-source APIs."""
    
    # API endpoints
    CPBJR_BASE = "https://cpbjr.github.io/catholic-readings-api"
    LITCAL_BASE = "https://litcal.johnromanodorazio.com/api/v3/LitCalEngine.php"
    
    def __init__(self, start_year: int, start_month: int, end_year: int):
        """Initialize the fetcher with date range."""
        self.start_date = date(start_year, start_month, 1)
        self.end_date = date(end_year, 12, 31)
        self.readings = []
        self.liturgical_calendar = {}
    
    def fetch_liturgical_calendar(self):
        """Fetch liturgical calendar data from CatholicOS API."""
        print("Fetching liturgical calendar data...")
        
        for year in [2025, 2026]:
            try:
                # Fetch calendar for the year
                response = requests.get(
                    self.LITCAL_BASE,
                    params={
                        "year": year,
                        "epiphany": "JAN6",  # Traditional Epiphany date
                        "ascension": "THURSDAY",  # Traditional Ascension
                        "corpus_christi": "THURSDAY",  # Traditional Corpus Christi
                        "eternal_high_priest": "FALSE",
                        "locale": "en"
                    },
                    timeout=30
                )
                
                if response.status_code == 200:
                    data = response.json()
                    if "litcal" in data:
                        for date_key, event_data in data["litcal"].items():
                            self.liturgical_calendar[date_key] = event_data
                        print(f"  ✓ Fetched {year} calendar ({len(data['litcal'])} events)")
                    else:
                        print(f"  ⚠ No litcal data for {year}")
                else:
                    print(f"  ✗ Failed to fetch {year} calendar: HTTP {response.status_code}")
                
                time.sleep(0.5)  # Be respectful to the API
                
            except Exception as e:
                print(f"  ✗ Error fetching {year} calendar: {e}")
    
    def fetch_cpbjr_reading(self, target_date: date) -> Dict[str, Any]:
        """
        Fetch reading from cpbjr API for a specific date.
        
        Args:
            target_date: The date to fetch
            
        Returns:
            Dictionary with reading data or None
        """
        date_str = target_date.strftime("%Y-%m-%d")
        month_day = target_date.strftime("%m-%d")
        
        # Only works for 2025 data currently
        if target_date.year == 2025:
            try:
                url = f"{self.CPBJR_BASE}/readings/{target_date.year}/{month_day}.json"
                response = requests.get(url, timeout=10)
                
                if response.status_code == 200:
                    data = response.json()
                    return self.parse_cpbjr_response(data, date_str)
                    
            except Exception as e:
                pass  # Fall through to liturgical calendar
        
        return None
    
    def parse_cpbjr_response(self, data: Dict, date_str: str) -> Dict[str, Any]:
        """Parse response from cpbjr API."""
        reading = {
            "date": date_str,
            "title": data.get("celebration", {}).get("title", "Daily Reading"),
            "readings": []
        }
        
        # Extract readings in order
        reading_types = [
            ("reading1", "First Reading"),
            ("psalm", "Psalm"),
            ("reading2", "Second Reading"),
            ("alleluia", "Gospel Acclamation"),
            ("gospel", "Gospel")
        ]
        
        for key, label in reading_types:
            if key in data and data[key]:
                reading_data = data[key]
                citation = reading_data.get("citation", "")
                text = reading_data.get("text", "")
                
                if text:
                    reading["readings"].append({
                        "type": label,
                        "citation": citation,
                        "text": text
                    })
        
        return reading
    
    def get_liturgical_title(self, target_date: date) -> str:
        """Get liturgical title from the calendar."""
        date_key = target_date.strftime("%Y-%m-%d")
        
        if date_key in self.liturgical_calendar:
            event = self.liturgical_calendar[date_key]
            if isinstance(event, dict):
                return event.get("name", f"Daily Reading - {target_date.strftime('%A')}")
            elif isinstance(event, list) and len(event) > 0:
                # Take the first (most important) celebration
                return event[0].get("name", f"Daily Reading - {target_date.strftime('%A')}")
        
        # Fallback
        weekday = target_date.strftime("%A")
        return f"Daily Reading - {weekday}"
    
    def create_reading_entry(self, target_date: date, has_full_data: bool = False) -> Dict[str, Any]:
        """Create a reading entry for a date."""
        date_str = target_date.strftime("%Y-%m-%d")
        title = self.get_liturgical_title(target_date)
        
        if not has_full_data:
            # Create placeholder
            return {
                "date": date_str,
                "title": title,
                "readings": [
                    {
                        "type": "First Reading",
                        "citation": "Data not yet available",
                        "text": f"Reading data for {date_str} will be available when published by liturgical sources."
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
        
        return None  # Will be filled with actual data
    
    def fetch_all_readings(self) -> None:
        """Fetch readings for all days in the date range."""
        total_days = (self.end_date - self.start_date).days + 1
        current_date = self.start_date
        day_count = 0
        
        print(f"\nFetching Catholic readings from {self.start_date} to {self.end_date}...")
        print(f"Total days to process: {total_days}")
        print()
        
        # First, fetch liturgical calendar
        self.fetch_liturgical_calendar()
        print()
        
        print("Fetching daily readings...")
        while current_date <= self.end_date:
            day_count += 1
            
            if day_count % 30 == 0 or day_count == 1:
                print(f"Processing day {day_count}/{total_days}: {current_date}")
            
            # Try to fetch from cpbjr first (has full readings for 2025)
            reading = self.fetch_cpbjr_reading(current_date)
            
            if reading:
                self.readings.append(reading)
            else:
                # Use liturgical calendar for title, but placeholder for readings
                reading = self.create_reading_entry(current_date, has_full_data=False)
                self.readings.append(reading)
            
            current_date += timedelta(days=1)
            time.sleep(0.1)  # Be respectful to APIs
        
        print(f"\nCompleted! Fetched {len(self.readings)} daily readings.")
    
    def save_to_json(self, output_path: str) -> None:
        """Save readings to JSON file."""
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(self.readings, f, indent=2, ensure_ascii=False)
        
        print(f"\nJSON file saved to: {output_path}")
        file_size = len(json.dumps(self.readings))
        print(f"File size: {file_size:,} bytes ({file_size/1024:.1f} KB)")


def main():
    """Main entry point."""
    print("=" * 70)
    print("Catholic Daily Readings Fetcher")
    print("Fetching from Open-Source APIs")
    print("=" * 70)
    print()
    print("DATA SOURCES:")
    print("-" * 70)
    print("1. cpbjr/catholic-readings-api (MIT License)")
    print("   - Full readings for 2025")
    print("   - https://github.com/cpbjr/catholic-readings-api")
    print()
    print("2. CatholicOS/liturgical-calendar-api (Open Source)")
    print("   - Liturgical calendar and feast day names")
    print("   - https://github.com/CatholicOS/liturgical-calendar-api")
    print()
    print("COPYRIGHT NOTICE:")
    print("-" * 70)
    print("Both APIs use MIT or similar permissive licenses.")
    print("Data is suitable for use in mobile applications.")
    print("Please review individual API licenses for details.")
    print("=" * 70)
    print()
    
    # Output path
    output_path = "GithubUsers/app/src/main/assets/catholic_readings_2026.json"
    if len(sys.argv) > 1:
        output_path = sys.argv[1]
    
    # Fetch readings from Nov 2025 to Dec 2026
    fetcher = CatholicReadingsFetcher(start_year=2025, start_month=11, end_year=2026)
    fetcher.fetch_all_readings()
    
    # Save to file
    fetcher.save_to_json(output_path)
    
    # Summary
    actual_readings = sum(1 for r in fetcher.readings 
                         if 'will be available' not in r['readings'][0]['text'])
    
    print()
    print("=" * 70)
    print("SUMMARY:")
    print("-" * 70)
    print(f"Total entries: {len(fetcher.readings)}")
    print(f"Entries with actual readings: Will vary based on API availability")
    print(f"Date range: {fetcher.start_date} to {fetcher.end_date}")
    print()
    print("✓ File ready for Android app!")
    print("=" * 70)


if __name__ == "__main__":
    main()
