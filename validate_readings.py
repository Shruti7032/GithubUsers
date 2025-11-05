#!/usr/bin/env python3
"""
Validation script for Catholic Daily Readings JSON file.

This script validates that the generated JSON file is complete and properly formatted.

Usage:
    python3 validate_readings.py [json_path]
    
    Arguments:
        json_path (optional): Path to JSON file to validate (default: GithubUsers/app/src/main/assets/catholic_readings_2026.json)
    
    Examples:
        python3 validate_readings.py
        python3 validate_readings.py readings_2027.json
"""

import json
import sys
from datetime import datetime, timedelta


def validate_json_structure(data):
    """Validate the basic JSON structure."""
    errors = []
    
    if not isinstance(data, list):
        errors.append("JSON root should be a list")
        return errors
    
    if len(data) == 0:
        errors.append("JSON is empty")
        return errors
    
    # Check first entry structure
    first_entry = data[0]
    required_keys = ['date', 'title', 'readings']
    
    for key in required_keys:
        if key not in first_entry:
            errors.append(f"Missing required key: {key}")
    
    if 'readings' in first_entry:
        if not isinstance(first_entry['readings'], list):
            errors.append("'readings' should be a list")
        elif len(first_entry['readings']) > 0:
            reading = first_entry['readings'][0]
            reading_keys = ['type', 'citation', 'text']
            for key in reading_keys:
                if key not in reading:
                    errors.append(f"Missing required key in reading: {key}")
    
    return errors


def validate_dates(data, year=2026):
    """Validate that all dates are present and sequential."""
    errors = []
    
    # Expected date range
    start_date = datetime(year, 1, 1)
    end_date = datetime(year, 12, 31)
    expected_days = (end_date - start_date).days + 1
    
    # Check total count
    if len(data) != expected_days:
        errors.append(f"Expected {expected_days} entries, found {len(data)}")
    
    # Check date format and sequence
    try:
        dates = [datetime.strptime(entry['date'], '%Y-%m-%d') for entry in data]
        
        # Check first and last dates
        if dates[0] != start_date:
            errors.append(f"First date should be {start_date.strftime('%Y-%m-%d')}, found {dates[0].strftime('%Y-%m-%d')}")
        
        if dates[-1] != end_date:
            errors.append(f"Last date should be {end_date.strftime('%Y-%m-%d')}, found {dates[-1].strftime('%Y-%m-%d')}")
        
        # Check for gaps
        for i in range(len(dates) - 1):
            expected_next = dates[i] + timedelta(days=1)
            if dates[i + 1] != expected_next:
                errors.append(f"Date gap found: {dates[i].strftime('%Y-%m-%d')} -> {dates[i+1].strftime('%Y-%m-%d')}")
        
        # Check for duplicates
        date_strings = [entry['date'] for entry in data]
        if len(date_strings) != len(set(date_strings)):
            errors.append("Duplicate dates found")
    
    except (KeyError, ValueError) as e:
        errors.append(f"Date validation error: {str(e)}")
    
    return errors


def validate_special_dates(data):
    """Validate that special liturgical dates have appropriate titles."""
    errors = []
    
    special_dates = {
        '2026-01-01': 'Mary',
        '2026-01-06': 'Epiphany',
        '2026-12-08': 'Immaculate',
        '2026-12-25': 'Christmas|Nativity',
    }
    
    for date_str, keyword in special_dates.items():
        entry = next((e for e in data if e['date'] == date_str), None)
        if entry:
            title = entry['title']
            keywords = keyword.split('|')
            if not any(kw.lower() in title.lower() for kw in keywords):
                errors.append(f"Date {date_str} should mention '{keyword}' in title, found: '{title}'")
        else:
            errors.append(f"Missing entry for special date: {date_str}")
    
    return errors


def validate_readings_content(data):
    """Validate that readings have content."""
    errors = []
    warnings = []
    
    for entry in data:
        date = entry.get('date', 'unknown')
        readings = entry.get('readings', [])
        
        if len(readings) == 0:
            errors.append(f"No readings for date: {date}")
        
        for i, reading in enumerate(readings):
            if not reading.get('type'):
                errors.append(f"Missing type for reading {i} on {date}")
            
            text = reading.get('text', '')
            if len(text.strip()) == 0:
                errors.append(f"Empty text for {reading.get('type', 'unknown')} on {date}")
            
            # Check for placeholder text
            if 'to be updated' in text.lower() or 'will be available when online' in text.lower():
                warnings.append(f"Placeholder text found for {reading.get('type', 'unknown')} on {date}")
    
    return errors, warnings


def main():
    """Main validation function."""
    import sys
    
    print("=" * 70)
    print("Catholic Daily Readings JSON Validator")
    print("=" * 70)
    print()
    
    # Allow custom path via command line argument
    json_path = 'GithubUsers/app/src/main/assets/catholic_readings_2026.json'
    if len(sys.argv) > 1:
        json_path = sys.argv[1]
    
    # Load JSON file
    print(f"Loading: {json_path}")
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print(f"✓ Successfully loaded JSON ({len(data)} entries)")
    except FileNotFoundError:
        print(f"✗ Error: File not found: {json_path}")
        return 1
    except json.JSONDecodeError as e:
        print(f"✗ Error: Invalid JSON: {str(e)}")
        return 1
    print()
    
    # Run validations
    all_errors = []
    all_warnings = []
    
    print("Running validations...")
    print("-" * 70)
    
    # Structure validation
    print("1. Validating JSON structure...", end=" ")
    errors = validate_json_structure(data)
    if errors:
        print("✗")
        all_errors.extend(errors)
    else:
        print("✓")
    
    # Date validation
    print("2. Validating dates...", end=" ")
    errors = validate_dates(data, year=2026)
    if errors:
        print("✗")
        all_errors.extend(errors)
    else:
        print("✓")
    
    # Special dates validation
    print("3. Validating special liturgical dates...", end=" ")
    errors = validate_special_dates(data)
    if errors:
        print("✗")
        all_errors.extend(errors)
    else:
        print("✓")
    
    # Content validation
    print("4. Validating readings content...", end=" ")
    errors, warnings = validate_readings_content(data)
    if errors:
        print("✗")
        all_errors.extend(errors)
    else:
        print("✓")
    all_warnings.extend(warnings)
    
    print()
    
    # Print results
    if all_errors:
        print("ERRORS FOUND:")
        print("-" * 70)
        for error in all_errors[:10]:  # Show first 10 errors
            print(f"  ✗ {error}")
        if len(all_errors) > 10:
            print(f"  ... and {len(all_errors) - 10} more errors")
        print()
    
    if all_warnings:
        print("WARNINGS:")
        print("-" * 70)
        # Only show a summary for placeholder warnings
        placeholder_count = sum(1 for w in all_warnings if 'placeholder' in w.lower())
        if placeholder_count > 0:
            print(f"  ⚠ {placeholder_count} entries have placeholder text")
            print(f"    (Run the generator with internet access to fetch real content)")
        other_warnings = [w for w in all_warnings if 'placeholder' not in w.lower()]
        for warning in other_warnings[:10]:
            print(f"  ⚠ {warning}")
        print()
    
    # Final summary
    print("=" * 70)
    if all_errors:
        print(f"VALIDATION FAILED: {len(all_errors)} error(s) found")
        return 1
    elif all_warnings:
        print(f"VALIDATION PASSED with {len(all_warnings)} warning(s)")
        print("Note: Warnings indicate placeholder content. Run generator with")
        print("      internet access to fetch actual readings from the API.")
        return 0
    else:
        print("VALIDATION PASSED: JSON file is complete and valid!")
        return 0


if __name__ == "__main__":
    sys.exit(main())
