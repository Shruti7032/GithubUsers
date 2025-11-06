#!/usr/bin/env python3
"""
Example usage of Catholic Daily Readings JSON file.

This script demonstrates how to load and query the readings data.
"""

import json
from datetime import datetime


def load_readings(json_path=None):
    """
    Load the readings from JSON file.
    
    Args:
        json_path: Path to JSON file. If None, uses default location.
    """
    if json_path is None:
        json_path = 'GithubUsers/app/src/main/assets/catholic_readings_2026.json'
    
    with open(json_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def get_reading_by_date(readings, date_str):
    """
    Get reading for a specific date.
    
    Args:
        readings: List of all readings
        date_str: Date in format 'YYYY-MM-DD'
    
    Returns:
        Reading dictionary or None if not found
    """
    return next((r for r in readings if r['date'] == date_str), None)


def get_readings_by_month(readings, year, month):
    """
    Get all readings for a specific month.
    
    Args:
        readings: List of all readings
        year: Year (e.g., 2026)
        month: Month (1-12)
    
    Returns:
        List of readings for that month
    """
    month_str = f"{year}-{month:02d}"
    return [r for r in readings if r['date'].startswith(month_str)]


def search_readings_by_keyword(readings, keyword):
    """
    Search for readings containing a keyword in title or text.
    
    Args:
        readings: List of all readings
        keyword: Keyword to search for
    
    Returns:
        List of matching readings
    """
    keyword_lower = keyword.lower()
    results = []
    
    for reading in readings:
        # Check title
        if keyword_lower in reading['title'].lower():
            results.append(reading)
            continue
        
        # Check readings text
        for r in reading['readings']:
            if keyword_lower in r['text'].lower() or keyword_lower in r['citation'].lower():
                results.append(reading)
                break
    
    return results


def print_reading(reading):
    """Pretty print a reading."""
    print(f"\n{'=' * 70}")
    print(f"Date: {reading['date']}")
    print(f"Title: {reading['title']}")
    print(f"{'=' * 70}")
    
    for r in reading['readings']:
        print(f"\n{r['type']}")
        if r['citation']:
            print(f"Citation: {r['citation']}")
        print(f"\n{r['text'][:200]}..." if len(r['text']) > 200 else f"\n{r['text']}")


def main():
    """Example usage demonstrations."""
    print("Catholic Daily Readings - Example Usage")
    print("=" * 70)
    
    # Load readings
    print("\n1. Loading readings...")
    readings = load_readings()
    print(f"   Loaded {len(readings)} daily readings")
    
    # Get specific date
    print("\n2. Get reading for New Year's Day 2026:")
    new_year = get_reading_by_date(readings, '2026-01-01')
    if new_year:
        print(f"   Title: {new_year['title']}")
        print(f"   Readings: {len(new_year['readings'])} parts")
    
    # Get readings for a month
    print("\n3. Get all readings for January 2026:")
    january_readings = get_readings_by_month(readings, 2026, 1)
    print(f"   Found {len(january_readings)} readings")
    print(f"   First: {january_readings[0]['date']} - {january_readings[0]['title']}")
    print(f"   Last: {january_readings[-1]['date']} - {january_readings[-1]['title']}")
    
    # Search by keyword
    print("\n4. Search for Christmas-related readings:")
    christmas_readings = search_readings_by_keyword(readings, 'Christmas')
    if christmas_readings:
        print(f"   Found {len(christmas_readings)} result(s):")
        for r in christmas_readings[:3]:
            print(f"   - {r['date']}: {r['title']}")
    
    # Get today's reading (if 2026)
    print("\n5. Get today's reading:")
    today = datetime.now().strftime('%Y-%m-%d')
    if today.startswith('2026'):
        today_reading = get_reading_by_date(readings, today)
        if today_reading:
            print(f"   Today ({today}): {today_reading['title']}")
    else:
        print(f"   Today is {today} (not in 2026 data)")
    
    # Display full reading
    print("\n6. Full display of New Year's Day reading:")
    if new_year:
        print_reading(new_year)
    
    print("\n" + "=" * 70)
    print("Example usage complete!")


if __name__ == "__main__":
    main()
