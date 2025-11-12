# Generic Quiz Data Converter (Word to JSON)

This script provides a **generic solution** to convert quiz data from Word documents (.docx) to structured JSON format with date-based organization for easy searching.

## Features

- ✅ Parse Word documents (.docx) containing quiz questions
- ✅ Support for multiple quizzes in a single document
- ✅ Automatic date detection and organization
- ✅ Date-indexed structure for fast searching
- ✅ Year-based organization (2026 data)
- ✅ Preserves questions, options, and answers
- ✅ Command-line interface for easy usage

## Installation

Install the required dependency:

```bash
pip install python-docx
```

## Usage

### Basic Usage

```bash
python3 convert_docx_quiz_to_json.py <path_to_word_document.docx> [output_file.json]
```

### Examples

```bash
# Convert a Word document to JSON with default output filename
python3 convert_docx_quiz_to_json.py quiz_data_2026.docx

# Convert with custom output filename
python3 convert_docx_quiz_to_json.py quiz_data_2026.docx my_quizzes.json

# Use with sample document
python3 convert_docx_quiz_to_json.py sample_quiz_2026.docx quizzes_2026.json
```

## Word Document Format

The script expects the Word document to follow this format:

### Date Header
```
April 5 Quiz:
```
or
```
Date: April 5
```
or simply
```
April 5
```

### Questions Section
```
Questions:
1. Who was preaching to the people in the first reading?
   A) Jesus
   B) Peter
   C) James
   D) John
```

### Answers Section
```
Answers:
1. B - Peter
2. C - What is above
3. B - Mary Magdalene
```

## Output JSON Structure

The script generates a JSON file with the following structure:

```json
{
  "year": 2026,
  "quizzes": [
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
  ],
  "quizzes_by_date": {
    "april_5": {
      "date": "April 5",
      "questions": [...]
    }
  }
}
```

### Structure Details

- **year**: Integer for the quiz year (2026)
- **quizzes**: Array of all quizzes in document order
- **quizzes_by_date**: Object with date keys for fast searching
  - Keys are lowercase with underscores (e.g., "april_5", "april_6")
  - Values are complete quiz objects

## Searching by Date

The `quizzes_by_date` structure makes it easy to search for specific dates:

```python
import json

# Load the JSON file
with open('quizzes_2026.json', 'r') as f:
    data = json.load(f)

# Search for a specific date
april_5_quiz = data['quizzes_by_date']['april_5']
print(f"Date: {april_5_quiz['date']}")
print(f"Questions: {len(april_5_quiz['questions'])}")

# Access specific question
first_question = april_5_quiz['questions'][0]
print(f"Q: {first_question['question']}")
print(f"A: {first_question['answer']}")
```

## Sample Document

A sample Word document (`sample_quiz_2026.docx`) is included for testing and reference.

## Error Handling

The script includes error handling for:
- Missing input file
- Invalid file format
- No quiz data found in document
- Missing python-docx library

## Benefits Over Static Script

Unlike the original `convert_quiz_to_json.py` which has hardcoded quiz data, this generic script:

1. **Accepts any Word document** - Just pass the file path
2. **Handles multiple quizzes** - Automatically detects all quizzes in the document
3. **Date-based indexing** - Easy searching by date
4. **Flexible format** - Supports various date header formats
5. **Reusable** - Can be used for any year's quiz data

## Files

- `convert_docx_quiz_to_json.py` - The generic converter script
- `sample_quiz_2026.docx` - Sample Word document with quiz data
- `quizzes_2026.json` - Example output from the sample document
- `README_GENERIC_CONVERTER.md` - This documentation file

## Comparison with Original Script

| Feature | Original Script | Generic Script |
|---------|----------------|----------------|
| Input Source | Hardcoded in script | Word document file |
| Flexibility | Fixed quizzes | Any number of quizzes |
| Reusability | One-time use | Reusable for any document |
| Date Search | Manual array search | Built-in date indexing |
| Year Support | Not specified | 2026 (configurable) |

## Troubleshooting

**Q: Script says "python-docx library is required"**  
A: Install it with `pip install python-docx`

**Q: No quiz data found**  
A: Check your Word document format matches the expected format (see above)

**Q: Answers are not matching questions**  
A: Ensure each quiz section has its own "Answers:" section immediately after the questions

**Q: Date not detected**  
A: Use one of the supported date formats: "April 5 Quiz:", "Date: April 5", or "April 5"

## License

This script is part of the GithubUsers project.
