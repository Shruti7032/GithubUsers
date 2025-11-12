#!/usr/bin/env python3
"""
Generic script to convert quiz data from Word document (.docx) to JSON format.
This script can parse a Word document containing quiz questions and convert them to 
a structured JSON format organized by date for easy searching.

Usage:
    python3 convert_docx_quiz_to_json.py <path_to_word_document.docx> [output_file.json]

Example:
    python3 convert_docx_quiz_to_json.py quiz_data_2026.docx quizzes_2026.json
"""

import sys
import json
import re
from pathlib import Path

try:
    from docx import Document
except ImportError:
    print("Error: python-docx library is required.")
    print("Install it using: pip install python-docx")
    sys.exit(1)


def parse_quiz_from_docx(docx_path):
    """
    Parse quiz data from a Word document.
    
    Expected format in Word document:
    - Date headers (e.g., "April 5 Quiz:", "April 5", "Date: April 5")
    - Questions numbered with 1., 2., etc.
    - Options labeled with A), B), C), D)
    - Answers section with format "1. B - Peter" or "Answer: Peter"
    
    Args:
        docx_path: Path to the Word document
        
    Returns:
        List of quiz dictionaries with date and questions
    """
    doc = Document(docx_path)
    quizzes = []
    current_quiz = None
    current_question = None
    answers_section = False
    answer_map = {}
    
    def apply_answers_to_quiz(quiz, ans_map):
        """Apply answer map to quiz questions."""
        for idx, question in enumerate(quiz['questions']):
            if idx in ans_map:
                question['answer'] = ans_map[idx]
    
    for para in doc.paragraphs:
        text = para.text.strip()
        
        if not text:
            continue
        
        # Detect date/quiz header
        date_match = re.search(r'(?:Date:\s*)?([A-Za-z]+\s+\d+)(?:\s+Quiz)?', text, re.IGNORECASE)
        if date_match and ('quiz' in text.lower() or 'date:' in text.lower() or re.match(r'^[A-Za-z]+\s+\d+$', text.strip())):
            # Apply answers to previous quiz if exists
            if current_quiz and current_quiz['questions']:
                apply_answers_to_quiz(current_quiz, answer_map)
                quizzes.append(current_quiz)
            
            # Start new quiz
            current_quiz = {
                'date': date_match.group(1).strip(),
                'questions': []
            }
            current_question = None
            answers_section = False
            answer_map = {}
            continue
        
        # Detect answers section
        if re.match(r'^Answers?:', text, re.IGNORECASE):
            answers_section = True
            continue
        
        # Parse answers in answers section
        if answers_section and current_quiz:
            answer_match = re.match(r'^(\d+)\.\s*([A-D])\s*[-–—]\s*(.+)$', text, re.IGNORECASE)
            if answer_match:
                q_num = int(answer_match.group(1)) - 1
                answer_text = answer_match.group(3).strip()
                answer_map[q_num] = answer_text
                continue
        
        # Parse question
        question_match = re.match(r'^(\d+)\.\s+(.+)$', text)
        if question_match and current_quiz is not None and not answers_section:
            q_num = int(question_match.group(1))
            q_text = question_match.group(2).strip()
            
            current_question = {
                'question': q_text,
                'options': [],
                'answer': ''
            }
            current_quiz['questions'].append(current_question)
            continue
        
        # Parse options
        option_match = re.match(r'^([A-D])\)\s+(.+)$', text, re.IGNORECASE)
        if option_match and current_question is not None:
            option_text = option_match.group(2).strip()
            current_question['options'].append(option_text)
            continue
    
    # Save last quiz with answers
    if current_quiz and current_quiz['questions']:
        apply_answers_to_quiz(current_quiz, answer_map)
        quizzes.append(current_quiz)
    
    return quizzes


def create_searchable_json(quizzes):
    """
    Create a JSON structure optimized for date-based searching.
    
    Args:
        quizzes: List of quiz dictionaries
        
    Returns:
        Dictionary with date as key for easy searching
    """
    searchable = {
        'year': 2026,
        'quizzes': quizzes,
        'quizzes_by_date': {}
    }
    
    # Create date-indexed structure for easy searching
    for quiz in quizzes:
        date_key = quiz['date'].lower().replace(' ', '_')
        searchable['quizzes_by_date'][date_key] = quiz
    
    return searchable


def main():
    """Main function to parse Word document and generate JSON."""
    
    # Check arguments
    if len(sys.argv) < 2:
        print("Usage: python3 convert_docx_quiz_to_json.py <path_to_word_document.docx> [output_file.json]")
        print("\nExample:")
        print("  python3 convert_docx_quiz_to_json.py quiz_data_2026.docx quizzes_2026.json")
        sys.exit(1)
    
    docx_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else 'quizzes_output.json'
    
    # Validate input file
    if not Path(docx_path).exists():
        print(f"Error: File '{docx_path}' not found.")
        sys.exit(1)
    
    if not docx_path.endswith('.docx'):
        print(f"Warning: File '{docx_path}' does not have .docx extension.")
    
    print(f"Reading quiz data from: {docx_path}")
    print("=" * 60)
    
    try:
        # Parse the document
        quizzes = parse_quiz_from_docx(docx_path)
        
        if not quizzes:
            print("Warning: No quiz data found in the document.")
            print("\nExpected format:")
            print("  - Date headers (e.g., 'April 5 Quiz:')")
            print("  - Questions numbered with 1., 2., etc.")
            print("  - Options labeled with A), B), C), D)")
            print("  - Answers section with format '1. B - Peter'")
            sys.exit(1)
        
        print(f"✓ Found {len(quizzes)} quiz(zes)")
        for quiz in quizzes:
            print(f"  - {quiz['date']}: {len(quiz['questions'])} questions")
        
        # Create searchable JSON structure
        output_data = create_searchable_json(quizzes)
        
        # Save to JSON file
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)
        
        print(f"\n✓ Successfully created: {output_path}")
        print("=" * 60)
        print("\nJSON Structure:")
        print("  - 'year': 2026")
        print("  - 'quizzes': Array of all quizzes in order")
        print("  - 'quizzes_by_date': Object with date keys for easy searching")
        print("\nExample usage to search by date:")
        print(f"  quiz = data['quizzes_by_date']['april_5']")
        
    except Exception as e:
        print(f"Error processing document: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
