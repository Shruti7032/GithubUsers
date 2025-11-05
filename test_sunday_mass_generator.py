#!/usr/bin/env python3
"""
Test script for Sunday Mass PDF Generator

This script verifies that the Sunday Mass PDF generator works correctly.
"""

import os
import sys
from datetime import datetime
import tempfile
import shutil

# Import the generator
from generate_sunday_mass_pdfs import SundayMassGenerator


def test_sunday_calculation():
    """Test that all Sundays are calculated correctly"""
    print("Test 1: Sunday Calculation")
    print("-" * 50)
    
    start_date = datetime(2025, 11, 1)
    end_date = datetime(2026, 12, 31)
    
    generator = SundayMassGenerator(start_date, end_date, output_dir="test_output")
    sundays = generator.get_all_sundays()
    
    # Verify we got the right number of Sundays
    expected_count = 61  # Calculated based on the date range
    actual_count = len(sundays)
    
    print(f"Expected Sundays: {expected_count}")
    print(f"Actual Sundays: {actual_count}")
    
    # Verify all dates are Sundays
    all_sundays = all(date.weekday() == 6 for date in sundays)
    print(f"All dates are Sundays: {all_sundays}")
    
    # Verify first and last Sunday
    first_sunday = sundays[0]
    last_sunday = sundays[-1]
    
    print(f"First Sunday: {first_sunday.strftime('%Y-%m-%d')} ({first_sunday.strftime('%A')})")
    print(f"Last Sunday: {last_sunday.strftime('%Y-%m-%d')} ({last_sunday.strftime('%A')})")
    
    assert actual_count == expected_count, f"Expected {expected_count} Sundays, got {actual_count}"
    assert all_sundays, "Not all dates are Sundays"
    assert first_sunday >= start_date, "First Sunday is before start date"
    assert last_sunday <= end_date, "Last Sunday is after end date"
    
    print("✓ Test 1 PASSED\n")
    return True


def test_pdf_generation():
    """Test that PDFs are generated correctly"""
    print("Test 2: PDF Generation")
    print("-" * 50)
    
    # Create a temporary directory for testing
    test_dir = tempfile.mkdtemp(prefix="mass_test_")
    
    try:
        # Generate PDFs for just a few Sundays
        start_date = datetime(2025, 11, 1)
        end_date = datetime(2025, 11, 30)  # Just November 2025
        
        generator = SundayMassGenerator(start_date, end_date, output_dir=test_dir)
        generated_files = generator.generate_all_pdfs()
        
        print(f"Generated {len(generated_files)} PDF files")
        
        # Verify files were created
        for filepath in generated_files:
            assert os.path.exists(filepath), f"PDF file not created: {filepath}"
            file_size = os.path.getsize(filepath)
            print(f"  {os.path.basename(filepath)}: {file_size} bytes")
            assert file_size > 0, f"PDF file is empty: {filepath}"
        
        print("✓ Test 2 PASSED\n")
        return True
        
    finally:
        # Clean up temporary directory
        if os.path.exists(test_dir):
            shutil.rmtree(test_dir)


def test_mass_data_structure():
    """Test that mass data structure is correct"""
    print("Test 3: Mass Data Structure")
    print("-" * 50)
    
    start_date = datetime(2025, 11, 1)
    end_date = datetime(2025, 11, 30)
    
    generator = SundayMassGenerator(start_date, end_date, output_dir="test_output")
    
    # Get a test Sunday
    test_date = datetime(2025, 11, 2)  # First Sunday in November 2025
    mass_data = generator.fetch_mass_readings(test_date)
    
    # Verify required fields
    required_fields = ['date', 'title', 'colour', 'readings']
    for field in required_fields:
        assert field in mass_data, f"Missing required field: {field}"
        print(f"✓ Field '{field}' present: {mass_data[field]}")
    
    # Verify readings structure
    assert isinstance(mass_data['readings'], list), "Readings should be a list"
    assert len(mass_data['readings']) > 0, "Readings should not be empty"
    
    print(f"Number of readings: {len(mass_data['readings'])}")
    
    print("✓ Test 3 PASSED\n")
    return True


def run_all_tests():
    """Run all tests"""
    print("=" * 70)
    print("Sunday Mass PDF Generator - Test Suite")
    print("=" * 70)
    print()
    
    tests = [
        test_sunday_calculation,
        test_pdf_generation,
        test_mass_data_structure
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
        except AssertionError as e:
            print(f"✗ Test FAILED: {e}\n")
            failed += 1
        except Exception as e:
            print(f"✗ Test ERROR: {e}\n")
            failed += 1
    
    print("=" * 70)
    print("Test Results")
    print("=" * 70)
    print(f"Passed: {passed}/{len(tests)}")
    print(f"Failed: {failed}/{len(tests)}")
    
    if failed == 0:
        print("\n✓ ALL TESTS PASSED!")
        return 0
    else:
        print(f"\n✗ {failed} TEST(S) FAILED")
        return 1


if __name__ == "__main__":
    sys.exit(run_all_tests())
