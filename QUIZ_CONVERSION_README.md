# Quiz Data Conversion Script

This directory contains a Python script to convert quiz data from Word document format to JSON format.

## Overview

The `convert_quiz_to_json.py` script converts quiz questions, options, and answers from text format into structured JSON files suitable for database or application use.

## Generated Files

Running the script generates three JSON files:

1. **quiz_april_5.json** - Contains the April 5 quiz
2. **quiz_april_6.json** - Contains the April 6 quiz  
3. **quizzes_combined.json** - Contains both quizzes in a single file

## How to Run

### Prerequisites

- Python 3.x installed on your system

### Running the Script

```bash
# Make the script executable (optional)
chmod +x convert_quiz_to_json.py

# Run with Python
python3 convert_quiz_to_json.py

# Or run directly if executable
./convert_quiz_to_json.py
```

### Expected Output

```
Converting quiz data to JSON format...

✓ Successfully created quiz_april_5.json
✓ Successfully created quiz_april_6.json
✓ Successfully created quizzes_combined.json

✓ All quiz files generated successfully!

Generated files:
  - quiz_april_5.json (April 5 quiz)
  - quiz_april_6.json (April 6 quiz)
  - quizzes_combined.json (Both quizzes)
```

## JSON Format

Each quiz file follows this structure:

```json
{
  "date": "April 5",
  "questions": [
    {
      "question": "Who was preaching to the people in the first reading?",
      "options": ["Jesus", "Peter", "James", "John"],
      "answer": "Peter"
    }
  ]
}
```

### Structure Details

- **date**: String identifying the quiz date
- **questions**: Array of question objects
  - **question**: The question text
  - **options**: Array of possible answers
  - **answer**: The correct answer (matches one of the options)

## Quiz Content

### April 5 Quiz
- 5 questions about biblical readings and events
- Topics: Peter's preaching, seeking what is above, Mary Magdalene, the empty tomb

### April 6 Quiz
- 5 questions about Pentecost and resurrection events
- Topics: Peter's Pentecost preaching, the Holy Spirit, the empty tomb, soldiers' account

## Usage in Applications

The generated JSON files can be:
- Imported into a database
- Used as seed data for applications
- Consumed by REST APIs
- Used in mobile or web applications for quiz features

## Modifying Quiz Data

To add or modify quiz data:

1. Open `convert_quiz_to_json.py`
2. Locate the `create_april_5_quiz()` or `create_april_6_quiz()` functions
3. Edit the quiz data structure
4. Run the script again to regenerate the JSON files

## License

This script is part of the GithubUsers project.
