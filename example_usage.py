#!/usr/bin/env python3
"""
Example Usage of Sunday Mass PDF Generator

This script demonstrates different ways to use the Sunday Mass PDF generator.
"""

from datetime import datetime
from generate_sunday_mass_pdfs import SundayMassGenerator


def example_1_default_usage():
    """
    Example 1: Generate PDFs for the default date range
    (November 1, 2025 to December 31, 2026)
    """
    print("Example 1: Default Usage")
    print("-" * 50)
    
    start_date = datetime(2025, 11, 1)
    end_date = datetime(2026, 12, 31)
    
    generator = SundayMassGenerator(start_date, end_date)
    files = generator.generate_all_pdfs()
    
    print(f"Generated {len(files)} PDF files")
    print()


def example_2_custom_date_range():
    """
    Example 2: Generate PDFs for a custom date range
    (Just Advent 2025)
    """
    print("Example 2: Custom Date Range (Advent 2025)")
    print("-" * 50)
    
    # Advent 2025: approximately Nov 30 - Dec 24
    start_date = datetime(2025, 11, 30)
    end_date = datetime(2025, 12, 24)
    
    generator = SundayMassGenerator(start_date, end_date, output_dir="advent_2025_pdfs")
    files = generator.generate_all_pdfs()
    
    print(f"Generated {len(files)} PDF files for Advent 2025")
    print()


def example_3_single_month():
    """
    Example 3: Generate PDFs for a single month
    """
    print("Example 3: Single Month (December 2025)")
    print("-" * 50)
    
    start_date = datetime(2025, 12, 1)
    end_date = datetime(2025, 12, 31)
    
    generator = SundayMassGenerator(start_date, end_date, output_dir="december_2025_pdfs")
    files = generator.generate_all_pdfs()
    
    print(f"Generated {len(files)} PDF files for December 2025")
    print()


def example_4_get_sundays_only():
    """
    Example 4: Just get the list of Sundays without generating PDFs
    """
    print("Example 4: Get Sunday Dates Only")
    print("-" * 50)
    
    start_date = datetime(2025, 11, 1)
    end_date = datetime(2025, 11, 30)
    
    generator = SundayMassGenerator(start_date, end_date)
    sundays = generator.get_all_sundays()
    
    print("Sundays in November 2025:")
    for sunday in sundays:
        print(f"  - {sunday.strftime('%B %d, %Y (%A)')}")
    print()


def example_5_single_sunday():
    """
    Example 5: Generate a PDF for a single specific Sunday
    """
    print("Example 5: Single Sunday (Christmas Day 2025)")
    print("-" * 50)
    
    generator = SundayMassGenerator(datetime(2025, 1, 1), datetime(2025, 12, 31), 
                                   output_dir="single_sunday_pdfs")
    
    # Generate for Christmas Sunday 2025
    christmas_date = datetime(2025, 12, 25)
    
    # Note: Dec 25, 2025 is a Thursday, so let's use the nearest Sunday
    # Let's use December 21, 2025 (4th Sunday of Advent)
    sunday_date = datetime(2025, 12, 21)
    
    mass_data = generator.fetch_mass_readings(sunday_date)
    pdf_file = generator.generate_pdf(mass_data)
    
    print(f"Generated single PDF: {pdf_file}")
    print()


if __name__ == "__main__":
    print("=" * 70)
    print("Sunday Mass PDF Generator - Usage Examples")
    print("=" * 70)
    print()
    
    # Uncomment the examples you want to run:
    
    # example_1_default_usage()
    # example_2_custom_date_range()
    # example_3_single_month()
    example_4_get_sundays_only()
    # example_5_single_sunday()
    
    print("=" * 70)
    print("For more information, see SUNDAY_MASS_README.md")
    print("=" * 70)
