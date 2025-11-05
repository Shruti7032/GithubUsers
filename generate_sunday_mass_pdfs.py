#!/usr/bin/env python3
"""
Catholic Sunday Mass PDF Generator

This script generates PDFs for Catholic Sunday Mass readings from November 1, 2025 to December 31, 2026.
It uses open-source libraries and public APIs to fetch liturgical readings.
"""

import os
import sys
from datetime import datetime, timedelta
from typing import List, Dict
import json

try:
    import requests
except ImportError:
    print("Error: 'requests' package not found.")
    print("Please install required dependencies:")
    print("  pip install -r requirements.txt")
    print("or")
    print("  pip install requests reportlab")
    sys.exit(1)

try:
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
    from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
except ImportError:
    print("Error: 'reportlab' package not found.")
    print("Please install required dependencies:")
    print("  pip install -r requirements.txt")
    print("or")
    print("  pip install requests reportlab")
    sys.exit(1)


class SundayMassGenerator:
    """Generator for Catholic Sunday Mass PDFs"""
    
    def __init__(self, start_date: datetime, end_date: datetime, output_dir: str = "assets"):
        self.start_date = start_date
        self.end_date = end_date
        self.output_dir = output_dir
        
        # Create output directory if it doesn't exist
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
    
    def get_all_sundays(self) -> List[datetime]:
        """Calculate all Sundays between start_date and end_date"""
        sundays = []
        current_date = self.start_date
        
        # Find the first Sunday
        while current_date.weekday() != 6:  # 6 = Sunday
            current_date += timedelta(days=1)
        
        # Collect all Sundays
        while current_date <= self.end_date:
            sundays.append(current_date)
            current_date += timedelta(days=7)
        
        return sundays
    
    def fetch_mass_readings(self, date: datetime) -> Dict:
        """
        Fetch Catholic Mass readings for a specific date.
        
        Uses the Catholic Liturgical Calendar API (open source).
        Alternative sources:
        - http://calapi.inadiutorium.cz/
        - https://bible.usccb.org/
        """
        
        # Format date for API
        date_str = date.strftime("%Y-%m-%d")
        
        # Try to fetch from Catholic Calendar API
        try:
            # Using the Catholic Liturgical Calendar API
            # Note: This API only supports HTTP (not HTTPS) as of 2025
            # Data is public liturgical information, not sensitive
            url = f"http://calapi.inadiutorium.cz/api/v0/en/calendars/default/{date_str}"
            response = requests.get(url, timeout=10, verify=True)
            
            if response.status_code == 200:
                data = response.json()
                return self._parse_calapi_response(data, date)
            else:
                print(f"Warning: Could not fetch data for {date_str} (Status: {response.status_code})")
                return self._get_default_readings(date)
        
        except Exception as e:
            print(f"Error fetching readings for {date_str}: {e}")
            return self._get_default_readings(date)
    
    def _parse_calapi_response(self, data: Dict, date: datetime) -> Dict:
        """Parse response from calapi.inadiutorium.cz"""
        
        celebrations = data.get('celebrations', [])
        
        if not celebrations:
            return self._get_default_readings(date)
        
        # Get the first celebration (usually the main one for Sunday)
        celebration = celebrations[0]
        
        title = celebration.get('title', 'Sunday Mass')
        colour = celebration.get('colour', 'green')
        rank = celebration.get('rank', '')
        
        # Extract readings if available
        readings = []
        if 'readings' in celebration:
            for reading in celebration['readings']:
                readings.append({
                    'citation': reading.get('citation', ''),
                    'reference': reading.get('reference', '')
                })
        
        return {
            'date': date,
            'title': title,
            'colour': colour,
            'rank': rank,
            'readings': readings,
            'season': data.get('season', 'Ordinary Time')
        }
    
    def _get_default_readings(self, date: datetime) -> Dict:
        """Return default structure when API is unavailable"""
        return {
            'date': date,
            'title': 'Sunday Mass',
            'colour': 'green',
            'rank': 'Sunday',
            'readings': [
                {'citation': 'First Reading', 'reference': 'To be determined'},
                {'citation': 'Responsorial Psalm', 'reference': 'To be determined'},
                {'citation': 'Second Reading', 'reference': 'To be determined'},
                {'citation': 'Gospel', 'reference': 'To be determined'}
            ],
            'season': 'Ordinary Time',
            'note': 'Readings to be confirmed from official sources'
        }
    
    def generate_pdf(self, mass_data: Dict):
        """Generate a PDF for a specific Sunday Mass"""
        
        date = mass_data['date']
        filename = f"Sunday_Mass_{date.strftime('%Y-%m-%d')}.pdf"
        filepath = os.path.join(self.output_dir, filename)
        
        # Create PDF document
        doc = SimpleDocTemplate(filepath, pagesize=letter,
                              rightMargin=72, leftMargin=72,
                              topMargin=72, bottomMargin=18)
        
        # Container for the 'Flowable' objects
        elements = []
        
        # Define styles
        styles = getSampleStyleSheet()
        
        # Custom styles
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor='darkblue',
            spaceAfter=30,
            alignment=TA_CENTER
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=16,
            textColor='darkred',
            spaceAfter=12,
            spaceBefore=12
        )
        
        normal_style = ParagraphStyle(
            'CustomNormal',
            parent=styles['Normal'],
            fontSize=12,
            spaceAfter=12,
            alignment=TA_JUSTIFY
        )
        
        # Add title
        title = f"Catholic Sunday Mass<br/>{date.strftime('%B %d, %Y')}"
        elements.append(Paragraph(title, title_style))
        elements.append(Spacer(1, 0.2*inch))
        
        # Add celebration information
        elements.append(Paragraph(f"<b>{mass_data['title']}</b>", heading_style))
        
        if 'season' in mass_data:
            elements.append(Paragraph(f"Liturgical Season: {mass_data['season']}", normal_style))
        
        if 'colour' in mass_data:
            elements.append(Paragraph(f"Liturgical Colour: {mass_data['colour'].title()}", normal_style))
        
        elements.append(Spacer(1, 0.3*inch))
        
        # Add readings
        elements.append(Paragraph("Mass Readings", heading_style))
        
        if mass_data.get('readings'):
            for idx, reading in enumerate(mass_data['readings'], 1):
                citation = reading.get('citation', f'Reading {idx}')
                reference = reading.get('reference', 'Reference not available')
                
                reading_text = f"<b>{citation}</b><br/>{reference}"
                elements.append(Paragraph(reading_text, normal_style))
                elements.append(Spacer(1, 0.15*inch))
        else:
            elements.append(Paragraph("Readings to be confirmed from official liturgical sources.", normal_style))
        
        # Add note if present
        if 'note' in mass_data:
            elements.append(Spacer(1, 0.3*inch))
            elements.append(Paragraph(f"<i>Note: {mass_data['note']}</i>", normal_style))
        
        # Add footer
        elements.append(Spacer(1, 0.5*inch))
        footer_style = ParagraphStyle(
            'Footer',
            parent=styles['Normal'],
            fontSize=9,
            textColor='gray',
            alignment=TA_CENTER
        )
        elements.append(Paragraph(
            "For complete readings, please refer to your local parish or visit usccb.org",
            footer_style
        ))
        
        # Build PDF
        doc.build(elements)
        print(f"Generated: {filename}")
        
        return filepath
    
    def generate_all_pdfs(self):
        """Generate PDFs for all Sundays in the date range"""
        
        sundays = self.get_all_sundays()
        print(f"\nFound {len(sundays)} Sundays between {self.start_date.strftime('%Y-%m-%d')} and {self.end_date.strftime('%Y-%m-%d')}")
        print(f"Generating PDFs in directory: {self.output_dir}\n")
        
        generated_files = []
        
        for sunday in sundays:
            print(f"Processing: {sunday.strftime('%B %d, %Y')}")
            mass_data = self.fetch_mass_readings(sunday)
            filepath = self.generate_pdf(mass_data)
            generated_files.append(filepath)
        
        print(f"\n✓ Successfully generated {len(generated_files)} PDF files!")
        print(f"  Output directory: {os.path.abspath(self.output_dir)}")
        
        return generated_files


def main():
    """Main entry point"""
    
    print("=" * 70)
    print("Catholic Sunday Mass PDF Generator")
    print("=" * 70)
    print()
    
    # Define date range: November 1, 2025 to December 31, 2026
    start_date = datetime(2025, 11, 1)
    end_date = datetime(2026, 12, 31)
    
    # Create generator instance
    generator = SundayMassGenerator(start_date, end_date)
    
    # Generate all PDFs
    try:
        generated_files = generator.generate_all_pdfs()
        
        print("\n" + "=" * 70)
        print("Summary")
        print("=" * 70)
        print(f"Start Date: {start_date.strftime('%B %d, %Y')}")
        print(f"End Date: {end_date.strftime('%B %d, %Y')}")
        print(f"Total PDFs Generated: {len(generated_files)}")
        print(f"Output Location: {os.path.abspath(generator.output_dir)}")
        print("\nAll PDF files have been successfully created!")
        
    except KeyboardInterrupt:
        print("\n\nProcess interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n\nError: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
