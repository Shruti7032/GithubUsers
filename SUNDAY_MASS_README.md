# Catholic Sunday Mass PDF Generator

This tool generates PDF documents for Catholic Sunday Mass readings from **November 1, 2025** to **December 31, 2026**.

## Features

- ✅ Automatically calculates all Sundays in the specified date range
- ✅ Fetches liturgical readings from open-source Catholic Calendar API
- ✅ Generates professional PDF documents for each Sunday
- ✅ Includes liturgical season, color, and celebration details
- ✅ Uses completely open-source libraries and resources

## Requirements

The script automatically installs required dependencies:
- Python 3.6 or higher
- `requests` - For API calls
- `reportlab` - For PDF generation

## Usage

### Basic Usage

Simply run the script:

```bash
python3 generate_sunday_mass_pdfs.py
```

The script will:
1. Calculate all Sundays between November 1, 2025 and December 31, 2026
2. Fetch Mass readings from the open-source Catholic Calendar API
3. Generate PDF files in the `sunday_mass_pdfs/` directory

### Output

PDFs are generated with filenames like:
- `Sunday_Mass_2025-11-02.pdf`
- `Sunday_Mass_2025-11-09.pdf`
- `Sunday_Mass_2025-11-16.pdf`
- etc.

Each PDF includes:
- Date and liturgical celebration title
- Liturgical season (e.g., Advent, Lent, Ordinary Time)
- Liturgical color (e.g., green, purple, white)
- Mass readings with references
- Additional notes when applicable

## Data Sources (Open Source)

This tool uses the following open-source resources:

### 1. Catholic Liturgical Calendar API
- **URL**: http://calapi.inadiutorium.cz/
- **License**: Open source
- **Description**: Provides liturgical calendar data including celebrations, readings, and colors

### 2. Alternative Sources
For complete reading texts, you can refer to:
- **USCCB Bible**: https://bible.usccb.org/
- **Universalis**: https://universalis.com/
- **iBreviary**: https://ibreviary.org/

## PDF Library (ReportLab)

- **Library**: ReportLab
- **License**: BSD License (Open Source)
- **Website**: https://www.reportlab.com/
- **Description**: Professional PDF generation for Python

## Customization

You can modify the script to:

### Change Date Range
Edit the `main()` function:
```python
start_date = datetime(2025, 11, 1)  # Change start date
end_date = datetime(2026, 12, 31)   # Change end date
```

### Change Output Directory
Modify the output directory:
```python
generator = SundayMassGenerator(start_date, end_date, output_dir="my_custom_folder")
```

### Customize PDF Style
Modify the `generate_pdf()` method to change:
- Font sizes and colors
- Page layout
- Content structure
- Add logos or images

## Example Output

```
======================================================================
Catholic Sunday Mass PDF Generator
======================================================================

Found 61 Sundays between 2025-11-01 and 2026-12-31
Generating PDFs in directory: sunday_mass_pdfs

Processing: November 02, 2025
Generated: Sunday_Mass_2025-11-02.pdf
Processing: November 09, 2025
Generated: Sunday_Mass_2025-11-09.pdf
...

✓ Successfully generated 61 PDF files!
  Output directory: /path/to/sunday_mass_pdfs
```

## Troubleshooting

### API Connection Issues
If the Catholic Calendar API is unavailable, the script will generate PDFs with placeholder readings that can be filled in later from official sources.

### Missing Dependencies
The script automatically installs missing dependencies. If you encounter issues, manually install them:
```bash
pip3 install requests reportlab
```

### Permission Issues
Ensure you have write permissions in the directory where the script is run.

## Notes

- The readings fetched from the API provide references but not full text
- For complete reading texts, please consult official Catholic liturgical resources
- PDFs are generated in letter size format (8.5" x 11")
- All generated content is based on the Roman Catholic liturgical calendar

## License

This script is provided as open-source software. Feel free to modify and distribute.

## Support

For issues with:
- **Script functionality**: Check the script comments and error messages
- **Liturgical accuracy**: Consult your local parish or diocese
- **Reading texts**: Visit usccb.org or your local Catholic resource

## Contributing

Improvements welcome! Consider:
- Adding support for different liturgical calendars (e.g., diocesan)
- Including full reading texts (with proper licensing)
- Supporting multiple languages
- Adding more customization options
- Generating compiled PDFs with all Sundays in one document

---

**Generated PDFs are for personal use. For liturgical ministry use, please consult official diocesan resources.**
