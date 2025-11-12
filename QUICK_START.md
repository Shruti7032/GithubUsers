# Quick Start Guide - Generic Quiz Converter

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
python3 convert_docx_quiz_to_json.py <your_document.docx> [output.json]
```

## Example

```bash
python3 convert_docx_quiz_to_json.py sample_quiz_2026.docx quizzes_2026.json
```

## Search by Date

```python
import json

with open('quizzes_2026.json') as f:
    data = json.load(f)

# Fast date lookup
april_5_quiz = data['quizzes_by_date']['april_5']
print(april_5_quiz['date'])  # "April 5"
print(len(april_5_quiz['questions']))  # 5
```

## Files Provided

- `convert_docx_quiz_to_json.py` - Generic converter script
- `sample_quiz_2026.docx` - Sample Word document
- `quizzes_2026.json` - Example output
- `requirements.txt` - Dependencies
- `README_GENERIC_CONVERTER.md` - Full documentation

## Output Structure

```json
{
  "year": 2026,
  "quizzes": [...],
  "quizzes_by_date": {
    "april_5": {...},
    "april_6": {...}
  }
}
```
