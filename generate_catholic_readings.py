#!/usr/bin/env python3
"""
Catholic Daily Readings Generator for 2026

This script fetches Catholic daily readings from a public API and generates
a JSON file for offline use in Android applications.

API Source: Catholic Readings API (various sources)
Output: catholic_readings_2026.json

Usage:
    python3 generate_catholic_readings.py

Requirements:
    - requests library (install with: pip install requests)
"""

import json
import sys
from datetime import datetime, timedelta
from typing import Dict, List, Any

try:
    import requests
except ImportError:
    print("Error: 'requests' library is required.")
    print("Install it with: pip install requests")
    sys.exit(1)


class CatholicReadingsGenerator:
    """Generator for Catholic daily readings JSON file."""
    
    # API endpoints to try (in order of preference)
    API_ENDPOINTS = [
        "https://api.daily-mass-readings.com/api/v1/mass-readings",
        "https://calapi.inadiutorium.cz/api/v0/en/calendars/default",
    ]
    
    def __init__(self, year: int = 2026):
        """
        Initialize the generator.
        
        Args:
            year: The year for which to generate readings (default: 2026)
        """
        self.year = year
        self.readings = []
    
    def fetch_reading_for_date(self, date: datetime) -> Dict[str, Any]:
        """
        Fetch reading for a specific date from the API.
        
        Args:
            date: The date for which to fetch readings
            
        Returns:
            Dictionary containing the reading data
        """
        date_str = date.strftime("%Y-%m-%d")
        
        # Try first API endpoint
        try:
            url = f"{self.API_ENDPOINTS[0]}?date={date_str}"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                return self.parse_api_response_v1(data, date_str)
        except Exception as e:
            print(f"Warning: Failed to fetch from primary API for {date_str}: {e}")
        
        # If first API fails, create a placeholder entry
        return self.create_placeholder_reading(date_str)
    
    def parse_api_response_v1(self, data: Dict, date_str: str) -> Dict[str, Any]:
        """
        Parse the API response from the daily-mass-readings API.
        
        Args:
            data: Raw API response data
            date_str: Date string in YYYY-MM-DD format
            
        Returns:
            Formatted reading data
        """
        reading = {
            "date": date_str,
            "title": data.get("title", "Daily Reading"),
            "readings": []
        }
        
        # Extract different reading types
        reading_types = [
            ("first_reading", "First Reading"),
            ("responsorial_psalm", "Psalm"),
            ("second_reading", "Second Reading"),
            ("gospel_acclamation", "Gospel Acclamation"),
            ("gospel", "Gospel")
        ]
        
        for key, label in reading_types:
            if key in data and data[key]:
                reading_data = data[key]
                if isinstance(reading_data, dict):
                    text = reading_data.get("text", "")
                    citation = reading_data.get("citation", "")
                    full_text = f"{citation}\n\n{text}" if citation else text
                    
                    if full_text.strip():
                        reading["readings"].append({
                            "type": label,
                            "citation": citation,
                            "text": full_text.strip()
                        })
        
        return reading
    
    def create_placeholder_reading(self, date_str: str) -> Dict[str, Any]:
        """
        Create a placeholder reading entry when API is unavailable.
        
        Args:
            date_str: Date string in YYYY-MM-DD format
            
        Returns:
            Placeholder reading data
        """
        # Determine the liturgical season or special feast
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        title = self.get_liturgical_title(date_obj)
        
        return {
            "date": date_str,
            "title": title,
            "readings": [
                {
                    "type": "First Reading",
                    "citation": "To be updated",
                    "text": "Reading content will be available when online."
                },
                {
                    "type": "Psalm",
                    "citation": "To be updated",
                    "text": "Psalm content will be available when online."
                },
                {
                    "type": "Gospel",
                    "citation": "To be updated",
                    "text": "Gospel content will be available when online."
                }
            ]
        }
    
    def get_liturgical_title(self, date: datetime) -> str:
        """
        Get the liturgical title for a given date.
        
        Args:
            date: The date object
            
        Returns:
            Liturgical title string
        """
        # Fixed feast days for 2026
        month_day = (date.month, date.day)
        
        special_days = {
            (1, 1): "Solemnity of Mary, Mother of God",
            (1, 6): "Epiphany of the Lord",
            (12, 8): "Immaculate Conception",
            (12, 25): "Nativity of the Lord (Christmas)",
            (11, 1): "All Saints",
            (11, 2): "All Souls' Day",
        }
        
        if month_day in special_days:
            return special_days[month_day]
        
        # Default weekday naming
        weekday = date.strftime("%A")
        return f"Daily Reading - {weekday}"
    
    def generate_all_readings(self) -> None:
        """Generate readings for all days in the specified year."""
        start_date = datetime(self.year, 1, 1)
        end_date = datetime(self.year, 12, 31)
        
        current_date = start_date
        day_count = 0
        
        print(f"Generating Catholic readings for {self.year}...")
        print(f"From {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")
        print()
        
        while current_date <= end_date:
            day_count += 1
            
            # Show progress
            if day_count % 30 == 0 or day_count == 1:
                print(f"Processing day {day_count}/365: {current_date.strftime('%Y-%m-%d')}")
            
            # Fetch reading for this date
            reading = self.fetch_reading_for_date(current_date)
            self.readings.append(reading)
            
            # Move to next day
            current_date += timedelta(days=1)
        
        print(f"\nCompleted! Generated {len(self.readings)} daily readings.")
    
    def save_to_json(self, output_path: str) -> None:
        """
        Save the readings to a JSON file.
        
        Args:
            output_path: Path where the JSON file should be saved
        """
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(self.readings, f, indent=2, ensure_ascii=False)
        
        print(f"\nJSON file saved to: {output_path}")
        print(f"File size: {len(json.dumps(self.readings))} bytes")


def main():
    """Main function to generate the Catholic readings JSON file."""
    print("=" * 60)
    print("Catholic Daily Readings Generator")
    print("=" * 60)
    print()
    print("COPYRIGHT AND USAGE NOTES:")
    print("-" * 60)
    print("The Catholic daily readings are typically in the public domain")
    print("or available for free use for religious and educational purposes.")
    print()
    print("Sources:")
    print("- USCCB (United States Conference of Catholic Bishops)")
    print("- Vatican resources")
    print("- Catholic Readings API projects")
    print()
    print("For commercial use or redistribution, please verify:")
    print("1. The specific translation (e.g., NABRE, RSV, etc.)")
    print("2. Copyright restrictions for that translation")
    print("3. Proper attribution requirements")
    print()
    print("This script is for educational and personal use.")
    print("=" * 60)
    print()
    
    # Generate readings
    generator = CatholicReadingsGenerator(year=2026)
    generator.generate_all_readings()
    
    # Save to assets folder (Android app location)
    output_path = "GithubUsers/app/src/main/assets/catholic_readings_2026.json"
    generator.save_to_json(output_path)
    
    print()
    print("SUCCESS! The readings have been generated.")
    print()
    print("Next steps:")
    print("1. Review the generated JSON file")
    print("2. Verify the readings are complete and accurate")
    print("3. If needed, update readings manually or re-run with internet access")
    print("4. The file is ready to be used in your Android app")


if __name__ == "__main__":
    main()
