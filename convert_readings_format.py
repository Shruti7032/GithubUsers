#!/usr/bin/env python3
"""
Convert Catholic Readings JSON between array and object formats.

This script converts between two JSON structures:
1. Array format: List of reading objects with embedded dates
2. Object format: Date-keyed object for direct lookup

Usage:
    python3 convert_readings_format.py input.json output.json [format]
    
    format: 'object' (default) or 'array'
"""

import json
import sys
from typing import Dict, List, Any


def array_to_object(readings_array: List[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
    """
    Convert array format to object format.
    
    Input:  [{"date": "2025-11-01", "title": "...", "readings": [...]}, ...]
    Output: {"2025-11-01": {"title": "...", "readings": [...]}, ...}
    """
    result = {}
    for reading in readings_array:
        if 'date' not in reading:
            print(f"Warning: Skipping entry without 'date' field: {reading.get('title', 'Unknown')}")
            continue
        
        date_key = reading['date']
        # Create new object without the date field
        reading_obj = {k: v for k, v in reading.items() if k != 'date'}
        result[date_key] = reading_obj
    
    return result


def object_to_array(readings_object: Dict[str, Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Convert object format to array format.
    
    Input:  {"2025-11-01": {"title": "...", "readings": [...]}, ...}
    Output: [{"date": "2025-11-01", "title": "...", "readings": [...]}, ...]
    """
    result = []
    for date_key, reading_data in sorted(readings_object.items()):
        # Create new object with date field
        reading_obj = {"date": date_key}
        reading_obj.update(reading_data)
        result.append(reading_obj)
    
    return result


def detect_format(data: Any) -> str:
    """Detect whether the data is in array or object format."""
    if isinstance(data, list):
        return 'array'
    elif isinstance(data, dict):
        # Check if keys look like dates
        if data:
            first_key = next(iter(data))
            # Simple check: date format YYYY-MM-DD
            if isinstance(first_key, str) and len(first_key) == 10 and first_key[4] == '-' and first_key[7] == '-':
                return 'object'
    return 'unknown'


def main():
    """Main function to handle command-line conversion."""
    if len(sys.argv) < 3:
        print("Usage: python3 convert_readings_format.py input.json output.json [format]")
        print("  format: 'object' (default) or 'array'")
        print("\nExamples:")
        print("  # Convert to object format (date-keyed)")
        print("  python3 convert_readings_format.py readings_array.json readings_object.json object")
        print("\n  # Convert to array format")
        print("  python3 convert_readings_format.py readings_object.json readings_array.json array")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    target_format = sys.argv[3].lower() if len(sys.argv) > 3 else 'object'
    
    if target_format not in ['array', 'object']:
        print(f"Error: Invalid format '{target_format}'. Must be 'array' or 'object'")
        sys.exit(1)
    
    # Load input file
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Error: Input file '{input_file}' not found")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in input file: {e}")
        sys.exit(1)
    
    # Detect current format
    current_format = detect_format(data)
    print(f"Detected input format: {current_format}")
    print(f"Target format: {target_format}")
    
    if current_format == 'unknown':
        print("Error: Could not detect format of input data")
        sys.exit(1)
    
    if current_format == target_format:
        print(f"Warning: Input is already in {target_format} format. Copying to output...")
        result = data
    else:
        # Convert
        print(f"Converting from {current_format} to {target_format}...")
        if target_format == 'object':
            result = array_to_object(data)
            print(f"✓ Converted {len(result)} readings to object format")
        else:
            result = object_to_array(data)
            print(f"✓ Converted {len(result)} readings to array format")
    
    # Save output file
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        print(f"✓ Saved to {output_file}")
    except Exception as e:
        print(f"Error saving output file: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
