# Catholic Daily Readings (Nov 2025 - Dec 2026)

This directory contains scripts to generate Catholic daily readings for offline use in Android applications.

> **📅 Date Range:** November 1, 2025 to December 31, 2026 (14 months, 426 days)
> 
> **📅 Note about Data:** USCCB has not yet published complete readings for 2025-2026. The generated JSON file includes **actual readings for major feast days** (Christmas, New Year, Epiphany, etc.) and placeholders for regular days. Regenerate the file when USCCB publishes full data.

## Quick Start

**For immediate use**: The JSON file is already generated at `GithubUsers/app/src/main/assets/catholic_readings_2026.json` with:
- ✅ **Date range**: November 1, 2025 to December 31, 2026 (426 days)
- ✅ **Actual readings** for major feast days (Christmas 2025 & 2026, New Year 2026, Epiphany 2026)
- ℹ️ Placeholders for regular days (USCCB hasn't published full data yet)

**To generate/update**:
```bash
# Generate with embedded sample data (works offline)
python3 generate_readings_with_sample_data.py

# Or try to fetch from USCCB (requires internet, may not have 2026 data yet)
pip install -r requirements.txt
python3 generate_catholic_readings.py
```

**To use in Android**: See the [Using in Android App](#using-in-android-app) section below.

## Overview

This solution provides:
- A Python script to fetch and generate Catholic daily readings
- JSON output covering 426 days (November 1, 2025 - December 31, 2026)
- Format suitable for offline Android app usage
- Instructions for regenerating/updating the readings

## Generated File

**Location**: `GithubUsers/app/src/main/assets/catholic_readings_2026.json`

**Format**:
```json
[
  {
    "date": "2026-01-01",
    "title": "Solemnity of Mary, Mother of God",
    "readings": [
      {
        "type": "First Reading",
        "citation": "Numbers 6:22-27",
        "text": "..."
      },
      {
        "type": "Psalm",
        "citation": "Psalm 67:2-3, 5, 6, 8",
        "text": "..."
      },
      {
        "type": "Gospel",
        "citation": "Luke 2:16-21",
        "text": "..."
      }
    ]
  },
  ...
]
```

## Requirements

### System Requirements
- Python 3.6 or higher
- Internet connection (for fetching readings from API)

### Python Dependencies
```bash
pip install -r requirements.txt
```

Or manually:
```bash
pip install requests
```

## Usage

### Generate Readings (Nov 2025 - Dec 2026)

#### Option 1: Fetch from Open-Source APIs (Recommended)

```bash
pip install requests
python3 fetch_readings_from_apis.py
```

This fetches actual readings from MIT-licensed open-source APIs:
- **cpbjr/catholic-readings-api**: Full readings for 2025
- **CatholicOS/liturgical-calendar-api**: Liturgical calendar and feast names
- Fetches real Scripture texts where available
- 426 days total (14 months)

**Best for**: Getting actual readings data from freely available sources.

### Option 1B: Fetch using Python + Selenium (Recommended for USCCB Direct Access - New!)

```bash
pip install selenium webdriver-manager
python3 fetch_readings_selenium.py
```

This uses Selenium (Python's browser automation tool) to fetch directly from USCCB:
- **Scrapes USCCB website directly** for the most current data
- Based on the get-catholic-daily-readings package logic
- Automatically manages ChromeDriver with webdriver-manager
- Fetches actual published readings when available

**Best for**: Getting real-time data directly from USCCB website.

**Note**: Requires Chrome/Chromium browser installed. The script respects USCCB's website with rate limiting.

### Option 1C: Fetch using Node.js (Alternative)

```bash
npm install
node fetch_readings_nodejs.js
```

This uses the **get-catholic-daily-readings** npm package (MIT license):
- Fetches directly from USCCB website
- Requires Node.js and browser automation (Puppeteer)
- May fetch more complete data when USCCB publishes it

**Best for**: Users comfortable with Node.js who need direct USCCB access.

**Note**: Requires Chromium/Chrome for browser automation. The package scrapes USCCB's website which may have usage limitations.

#### Option 2: Generate with Embedded Sample Data

```bash
python3 generate_readings_with_sample_data.py
```

This generates a complete JSON file covering Nov 2025 - Dec 2026 with:
- Actual Catholic readings for major feast days (Christmas, New Year, Epiphany, All Saints, etc.)
- Placeholder text for regular days with instructions to update
- 426 days total (14 months)

**Best for**: Offline use when internet access is unavailable.

#### Option 3: Fetch from USCCB (When Data is Available)

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the USCCB generator**:
   ```bash
   python3 generate_catholic_readings.py
   ```

**Best for**: When USCCB publishes complete 2025-2026 readings data.

**Output**: Both scripts create `catholic_readings_2026.json` in `GithubUsers/app/src/main/assets/`

**Note**: The repository already includes a generated JSON file with actual readings for major feast days.

### Generate Readings for a Different Year

To generate readings for a different year, modify the script:

```python
# In generate_catholic_readings.py, change the year parameter:
generator = CatholicReadingsGenerator(year=2027)  # Change year here
```

Or create a custom script:

```python
from generate_catholic_readings import CatholicReadingsGenerator

generator = CatholicReadingsGenerator(year=2027)
generator.generate_all_readings()
generator.save_to_json("catholic_readings_2027.json")
```

## API Sources

The script attempts to fetch readings from the following public APIs:

1. **Daily Mass Readings API**
   - URL: https://api.daily-mass-readings.com/api/v1/mass-readings
   - Documentation: https://cpbjr.github.io/catholic-readings-api/

2. **Fallback**: If the API is unavailable, the script generates placeholder entries that can be manually updated later.

### Alternative Sources

If the primary API is unavailable, you can also fetch readings from:

- **USCCB (United States Conference of Catholic Bishops)**
  - Website: https://bible.usccb.org/daily-bible-reading
  
- **Universalis**
  - Website: https://universalis.com/

- **Catholic.org Daily Readings**
  - Website: https://www.catholic.org/bible/daily_reading/

## Copyright and Legal Notes

### Content Usage

The Catholic daily readings and Scripture texts have varying copyright statuses depending on the translation:

#### Public Domain Translations
- **Douay-Rheims** (pre-1923 editions)
- **King James Version (KJV)**

#### Copyrighted Translations (Require Permission)
- **New American Bible, Revised Edition (NABRE)** - © USCCB
- **New Revised Standard Version (NRSV)** - © National Council of Churches
- **Jerusalem Bible** - © Darton, Longman & Todd

### Usage Guidelines

1. **Personal/Educational Use**: Generally permitted for most translations
2. **Religious/Liturgical Use**: Usually allowed with proper attribution
3. **Commercial Use**: May require licensing depending on the translation

### Recommendations for App Distribution

1. **Use Public Domain Translations**: Safest option for redistribution
2. **Obtain Permissions**: For copyrighted translations, contact copyright holders
3. **Provide Attribution**: Always credit the translation and source
4. **Check Local Laws**: Copyright laws vary by jurisdiction

### Attribution Template

Include in your app:

```
Catholic Daily Readings
Scripture texts from [Translation Name]
© [Copyright Holder]
Used with permission for personal/educational/religious purposes

API Source: [API Name/URL]
```

### Disclaimer

**This script and data are provided for personal, educational, and religious use.** Users are responsible for:
- Verifying copyright status of specific translations
- Obtaining necessary permissions for commercial use
- Providing proper attribution
- Complying with local copyright laws

The script author assumes no liability for copyright infringement resulting from improper use.

## Troubleshooting

### Common Issues

**Problem**: Script fails with "requests module not found"
```bash
Solution: pip install requests
```

**Problem**: API returns no data or errors
```
Solution: The script will generate placeholder entries. You can:
1. Try again later when the API is available
2. Manually update the JSON file
3. Use alternative data sources
```

**Problem**: JSON file is too large
```
Solution: The file size is expected to be 1-5 MB depending on content length.
This is acceptable for offline Android apps.
```

### Validation

**Recommended**: Use the validation script to check the JSON file:

```bash
python3 validate_readings.py
```

This will verify:
- JSON structure is correct
- All 426 days are present (Nov 1, 2025 - Dec 31, 2026, no gaps, no duplicates)
- Special liturgical dates are properly titled
- Readings have content

**Alternative**: Quick JSON validation:

```bash
python3 -m json.tool GithubUsers/app/src/main/assets/catholic_readings_2026.json > /dev/null && echo "✓ Valid JSON"
```

**Check entry count**:

```bash
python3 -c "import json; data=json.load(open('GithubUsers/app/src/main/assets/catholic_readings_2026.json')); print(f'Total days: {len(data)}')"
```

## Using in Android App

### Step 1: Add Gson Dependency

Add to your `build.gradle` (app level):
```gradle
dependencies {
    implementation 'com.google.code.gson:gson:2.10.1'
}
```

### Step 2: Create Data Classes

```kotlin
data class DailyReading(
    val date: String,
    val title: String,
    val readings: List<Reading>
)

data class Reading(
    val type: String,
    val citation: String,
    val text: String
)
```

### Step 3: Load the JSON from Assets

```kotlin
import android.content.Context
import com.google.gson.Gson
import com.google.gson.reflect.TypeToken
import java.io.IOException

class CatholicReadingsLoader(private val context: Context) {
    
    fun loadCatholicReadings(): List<DailyReading> {
        return try {
            val json = context.assets.open("catholic_readings_2026.json")
                .bufferedReader()
                .use { it.readText() }
            
            val gson = Gson()
            val type = object : TypeToken<List<DailyReading>>() {}.type
            gson.fromJson(json, type)
        } catch (e: IOException) {
            e.printStackTrace()
            emptyList()
        }
    }
    
    fun getReadingForDate(date: String): DailyReading? {
        val allReadings = loadCatholicReadings()
        return allReadings.find { it.date == date }
    }
    
    fun getTodayReading(): DailyReading? {
        val today = java.time.LocalDate.now().toString() // Format: "2026-01-01"
        return getReadingForDate(today)
    }
}
```

### Step 4: Usage Example

```kotlin
// In your Activity or Fragment:
class ReadingsActivity : AppCompatActivity() {
    
    private lateinit var readingsLoader: CatholicReadingsLoader
    
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_readings)
        
        readingsLoader = CatholicReadingsLoader(this)
        
        // Load today's reading
        val todayReading = readingsLoader.getTodayReading()
        todayReading?.let { reading ->
            displayReading(reading)
        }
    }
    
    private fun displayReading(reading: DailyReading) {
        // Display the reading in your UI
        findViewById<TextView>(R.id.dateTextView).text = reading.date
        findViewById<TextView>(R.id.titleTextView).text = reading.title
        
        // Display each reading type
        reading.readings.forEach { readingItem ->
            // Add to RecyclerView or display in TextViews
            Log.d("Reading", "${readingItem.type}: ${readingItem.text}")
        }
    }
}
```

### Step 5: Query Specific Dates

```kotlin
// Get reading for a specific date
val newYearReading = readingsLoader.getReadingForDate("2026-01-01")

// Get reading for Christmas
val christmasReading = readingsLoader.getReadingForDate("2026-12-25")

// Display the title
newYearReading?.let {
    println("${it.date}: ${it.title}")
    it.readings.forEach { reading ->
        println("  ${reading.type}: ${reading.citation}")
    }
}
```

### Performance Tips

**For better performance**, cache the loaded readings:

```kotlin
object CatholicReadingsCache {
    private var cachedReadings: List<DailyReading>? = null
    
    fun getReadings(context: Context): List<DailyReading> {
        if (cachedReadings == null) {
            cachedReadings = CatholicReadingsLoader(context).loadCatholicReadings()
        }
        return cachedReadings ?: emptyList()
    }
}
```

## Maintenance and Updates

### Annual Updates

Each year, regenerate the readings:

1. Update the year in the script or parameter
2. Run the generation script
3. Update the asset filename in your Android app
4. Test the new data

### Incremental Updates

To update specific dates:

1. Edit the JSON file directly
2. Maintain the same structure
3. Validate JSON after editing

## Additional Resources

### Catholic Resources
- [Awesome Catholic (GitHub)](https://github.com/servusDei2018/awesome-catholic)
- [USCCB Daily Readings](https://bible.usccb.org/daily-bible-reading)
- [Liturgical Calendar](https://www.liturgicalcalendar.com/)

### Development Resources
- [Android Assets Documentation](https://developer.android.com/guide/topics/resources/providing-resources)
- [Gson JSON Library](https://github.com/google/gson)

## License

This script is provided as-is for educational purposes. Scripture content copyright belongs to respective translation copyright holders. See COPYRIGHT AND LEGAL NOTES section above.

## Support

For issues or questions:
1. Check the Troubleshooting section
2. Review API documentation
3. Consult Catholic resource websites
4. Open an issue in the repository

---

**Last Updated**: 2026-01-01
**Script Version**: 1.0
**Target Year**: 2026
