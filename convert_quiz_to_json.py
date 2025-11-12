#!/usr/bin/env python3
"""
Script to convert quiz data from Word document to JSON format.
This script generates JSON files for April 5 and April 6 quizzes.
"""

import json
import os

def create_april_5_quiz():
    """Create the April 5 quiz data structure."""
    return {
        "date": "April 5",
        "questions": [
            {
                "question": "Who was preaching to the people in the first reading?",
                "options": ["Jesus", "Peter", "James", "John"],
                "answer": "Peter"
            },
            {
                "question": "In the second reading, what are we told to seek?",
                "options": ["Treasure on earth", "Fame and fortune", "What is above", "Missing items"],
                "answer": "What is above"
            },
            {
                "question": "Who told Peter and the other disciple that Jesus was not in the tomb?",
                "options": ["John the Baptist", "Mary Magdalene", "Andrew", "The Pharisees"],
                "answer": "Mary Magdalene"
            },
            {
                "question": "What did Peter and the other disciple do when they learned that Jesus was not in the tomb?",
                "options": ["Ran to the tomb", "Went fishing", "Cried", "Hid from the Romans"],
                "answer": "Ran to the tomb"
            },
            {
                "question": "What did the other disciple do when he saw the empty tomb?",
                "options": ["Shouted", "Cried", "Fainted", "Believed"],
                "answer": "Believed"
            }
        ]
    }

def create_april_6_quiz():
    """Create the April 6 quiz data structure."""
    return {
        "date": "April 6",
        "questions": [
            {
                "question": "Who preached to the people on Pentecost?",
                "options": ["Jesus", "Peter", "John", "Mary Magdalene"],
                "answer": "Peter"
            },
            {
                "question": "Whom did God send, as He had promised, on Pentecost?",
                "options": ["Jesus", "David", "Peter", "The Holy Spirit"],
                "answer": "The Holy Spirit"
            },
            {
                "question": "Jesus told the women leaving the tomb not to be ___________.",
                "options": ["Afraid", "Quiet", "Angry", "Silly"],
                "answer": "Afraid"
            },
            {
                "question": "What did the Jewish priests tell the soldiers to do?",
                "options": ["Attack", "Lie", "Go to sleep", "Run away"],
                "answer": "Lie"
            },
            {
                "question": "What did the soldiers say happened to Jesus's body?",
                "options": ["They buried it", "He rose from the dead", "The Jewish priests lost it", "The disciples stole it"],
                "answer": "The disciples stole it"
            }
        ]
    }

def save_quiz_to_json(quiz_data, filename):
    """
    Save quiz data to a JSON file.
    
    Args:
        quiz_data: Dictionary containing quiz data
        filename: Name of the output JSON file
    """
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(quiz_data, f, indent=2, ensure_ascii=False)
    print(f"✓ Successfully created {filename}")

def main():
    """Main function to generate quiz JSON files."""
    print("Converting quiz data to JSON format...\n")
    
    # Create quiz data
    april_5_quiz = create_april_5_quiz()
    april_6_quiz = create_april_6_quiz()
    
    # Save to JSON files
    save_quiz_to_json(april_5_quiz, "quiz_april_5.json")
    save_quiz_to_json(april_6_quiz, "quiz_april_6.json")
    
    # Create a combined file with both quizzes
    combined_quizzes = {
        "quizzes": [april_5_quiz, april_6_quiz]
    }
    save_quiz_to_json(combined_quizzes, "quizzes_combined.json")
    
    print("\n✓ All quiz files generated successfully!")
    print("\nGenerated files:")
    print("  - quiz_april_5.json (April 5 quiz)")
    print("  - quiz_april_6.json (April 6 quiz)")
    print("  - quizzes_combined.json (Both quizzes)")

if __name__ == "__main__":
    main()
