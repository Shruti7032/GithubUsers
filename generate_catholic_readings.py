#!/usr/bin/env python3
"""
Catholic Daily Readings Generator - USCCB Data Source

This script generates Catholic daily readings using the catholic-mass-readings package
which fetches data from USCCB (United States Conference of Catholic Bishops).

NOTE: For 2026, USCCB data is not yet published. Use generate_readings_with_sample_data.py
      instead, which includes actual readings for major feast days.

Output: catholic_readings_2026.json

Usage:
    python3 generate_catholic_readings.py [year] [output_path]
    
    Arguments:
        year (optional): Year for which to generate readings (default: 2026)
        output_path (optional): Output JSON file path (default: GithubUsers/app/src/main/assets/catholic_readings_2026.json)
    
    Examples:
        python3 generate_catholic_readings.py
        python3 generate_catholic_readings.py 2027
        python3 generate_catholic_readings.py 2027 readings_2027.json

Requirements:
    - catholic-mass-readings library (install with: pip install catholic-mass-readings)
"""

import json
import sys
import asyncio
from datetime import datetime, timedelta, date
from typing import Dict, List, Any

try:
    from catholic_mass_readings import USCCB
except ImportError:
    print("Error: 'catholic-mass-readings' library is required.")
    print("Install it with: pip install catholic-mass-readings")
    sys.exit(1)


class CatholicReadingsGenerator:
    """Generator for Catholic daily readings JSON file using USCCB data."""
    
    def __init__(self, year: int = 2026):
        """
        Initialize the generator.
        
        Args:
            year: The year for which to generate readings (default: 2026)
        """
        self.year = year
        self.readings = []
        self.usccb = USCCB()
    
    async def fetch_reading_for_date(self, target_date: date) -> Dict[str, Any]:
        """
        Fetch reading for a specific date from USCCB.
        
        Args:
            target_date: The date for which to fetch readings
            
        Returns:
            Dictionary containing the reading data
        """
        date_str = target_date.strftime("%Y-%m-%d")
        
        try:
            # Fetch mass reading from USCCB
            mass = await self.usccb.get_mass_from_date(target_date)
            
            if mass:
                return self.parse_mass_reading(mass, date_str)
            else:
                # If no data available, create placeholder
                return self.create_placeholder_reading(date_str, target_date)
        except Exception as e:
            print(f"Warning: Failed to fetch reading for {date_str}: {e}")
            return self.create_placeholder_reading(date_str, target_date)
    
    def parse_mass_reading(self, mass, date_str: str) -> Dict[str, Any]:
        """
        Parse the mass reading from USCCB.
        
        Args:
            mass: Mass object from USCCB
            date_str: Date string in YYYY-MM-DD format
            
        Returns:
            Formatted reading data
        """
        reading = {
            "date": date_str,
            "title": mass.title if hasattr(mass, 'title') and mass.title else "Daily Reading",
            "readings": []
        }
        
        # Extract first reading
        if hasattr(mass, 'first_reading') and mass.first_reading:
            fr = mass.first_reading
            reading["readings"].append({
                "type": "First Reading",
                "citation": fr.citation if hasattr(fr, 'citation') else "",
                "text": fr.text if hasattr(fr, 'text') else ""
            })
        
        # Extract responsorial psalm
        if hasattr(mass, 'responsorial_psalm') and mass.responsorial_psalm:
            ps = mass.responsorial_psalm
            reading["readings"].append({
                "type": "Psalm",
                "citation": ps.citation if hasattr(ps, 'citation') else "",
                "text": ps.text if hasattr(ps, 'text') else ""
            })
        
        # Extract second reading (if available)
        if hasattr(mass, 'second_reading') and mass.second_reading:
            sr = mass.second_reading
            reading["readings"].append({
                "type": "Second Reading",
                "citation": sr.citation if hasattr(sr, 'citation') else "",
                "text": sr.text if hasattr(sr, 'text') else ""
            })
        
        # Extract gospel acclamation (if available)
        if hasattr(mass, 'gospel_acclamation') and mass.gospel_acclamation:
            ga = mass.gospel_acclamation
            reading["readings"].append({
                "type": "Gospel Acclamation",
                "citation": ga.citation if hasattr(ga, 'citation') else "",
                "text": ga.text if hasattr(ga, 'text') else ""
            })
        
        # Extract gospel
        if hasattr(mass, 'gospel') and mass.gospel:
            gp = mass.gospel
            reading["readings"].append({
                "type": "Gospel",
                "citation": gp.citation if hasattr(gp, 'citation') else "",
                "text": gp.text if hasattr(gp, 'text') else ""
            })
        
        return reading
    
    def create_placeholder_reading(self, date_str: str, date_obj: date) -> Dict[str, Any]:
        """
        Create a placeholder reading entry when data is unavailable.
        
        Args:
            date_str: Date string in YYYY-MM-DD format
            date_obj: Date object
            
        Returns:
            Placeholder reading data with liturgical title
        """
        title = self.get_liturgical_title(date_obj)
        
        return {
            "date": date_str,
            "title": title,
            "readings": [
                {
                    "type": "First Reading",
                    "citation": "Data not yet available",
                    "text": f"Reading data for {date_str} is not yet published by USCCB. Please check back closer to this date or regenerate this file."
                },
                {
                    "type": "Psalm",
                    "citation": "Data not yet available",
                    "text": f"Psalm for {date_str} will be available closer to the date."
                },
                {
                    "type": "Gospel",
                    "citation": "Data not yet available",
                    "text": f"Gospel reading for {date_str} will be available closer to the date."
                }
            ]
        }
    
    def get_liturgical_title(self, target_date: date) -> str:
        """
        Get the liturgical title for a given date.
        
        Args:
            target_date: The date object
            
        Returns:
            Liturgical title string
        """
        # Fixed feast days for 2026
        month_day = (target_date.month, target_date.day)
        
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
        weekday = target_date.strftime("%A")
        return f"Daily Reading - {weekday}"
    
    async def generate_all_readings(self) -> None:
        """Generate readings for all days in the specified year."""
        start_date = date(self.year, 1, 1)
        end_date = date(self.year, 12, 31)
        
        current_date = start_date
        day_count = 0
        
        print(f"Generating Catholic readings for {self.year}...")
        print(f"From {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")
        print(f"Using USCCB (United States Conference of Catholic Bishops) data source")
        print()
        
        while current_date <= end_date:
            day_count += 1
            
            # Show progress
            if day_count % 30 == 0 or day_count == 1:
                print(f"Processing day {day_count}/365: {current_date.strftime('%Y-%m-%d')}")
            
            # Fetch reading for this date
            reading = await self.fetch_reading_for_date(current_date)
            self.readings.append(reading)
            
            # Move to next day
            current_date = date(current_date.year, current_date.month, current_date.day) + timedelta(days=1)
        
        print(f"\nCompleted! Generated {len(self.readings)} daily readings.")
        
        # Close the USCCB connection
        await self.usccb.close()
    
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


async def main_async():
    """Main async function to generate the Catholic readings JSON file."""
    print("=" * 60)
    print("Catholic Daily Readings Generator")
    print("=" * 60)
    print()
    print("COPYRIGHT AND USAGE NOTES:")
    print("-" * 60)
    print("The Catholic daily readings are sourced from:")
    print("- USCCB (United States Conference of Catholic Bishops)")
    print("- Using the New American Bible, Revised Edition (NABRE)")
    print()
    print("The NABRE translation is copyrighted by the USCCB.")
    print("For use in apps:")
    print("1. Personal, educational, and religious use is generally permitted")
    print("2. For commercial use, contact USCCB for licensing")
    print("3. Proper attribution should be provided:")
    print("   'Scripture texts from the New American Bible, Revised")
    print("    Edition © 2010, 1991, 1986, 1970 Confraternity of")
    print("    Christian Doctrine, Washington, D.C.'")
    print()
    print("This script is for educational and personal use.")
    print("=" * 60)
    print()
    
    # Parse command line arguments
    year = 2026
    output_path = "GithubUsers/app/src/main/assets/catholic_readings_2026.json"
    
    if len(sys.argv) > 1:
        try:
            year = int(sys.argv[1])
        except ValueError:
            print(f"Warning: Invalid year '{sys.argv[1]}', using default 2026")
    
    if len(sys.argv) > 2:
        output_path = sys.argv[2]
    
    # Generate readings
    generator = CatholicReadingsGenerator(year=year)
    await generator.generate_all_readings()
    
    # Save to assets folder (Android app location)
    generator.save_to_json(output_path)
    
    print()
    print("SUCCESS! The readings have been generated.")
    print()
    print("Next steps:")
    print("1. Review the generated JSON file")
    print("2. Verify the readings are complete and accurate")
    print("3. The file is ready to be used in your Android app")
    print()
    print("Note: If some dates show 'Data not yet available', it means")
    print("      USCCB has not published those readings yet. Re-run the")
    print("      script closer to those dates to fetch actual content.")


def main():
    """Entry point for the script."""
    asyncio.run(main_async())


if __name__ == "__main__":
    main()
