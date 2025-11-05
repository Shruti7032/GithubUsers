# Catholic Daily Readings for 2026

This directory contains a script to generate Catholic daily readings for offline use in Android applications.

## Quick Start

**For immediate use**: The JSON file is already generated at `GithubUsers/app/src/main/assets/catholic_readings_2026.json` with 365 days of placeholder readings.

**To fetch real content** (requires internet):
```bash
pip install -r requirements.txt
python3 generate_catholic_readings.py
```

**To use in Android**: See the [Using in Android App](#using-in-android-app) section below.

## Overview

This solution provides:
- A Python script to fetch and generate Catholic daily readings
- JSON output covering all 365 days of 2026 (January 1 - December 31)
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

### Generate Readings for 2026

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the generator script**:
   ```bash
   python3 generate_catholic_readings.py
   ```

3. **Output**: The script will create `catholic_readings_2026.json` in the `GithubUsers/app/src/main/assets/` directory.

**Note**: The repository already includes a generated JSON file. You only need to run the script if you want to fetch fresh content from the API or regenerate the file.

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

To validate the generated JSON:

```bash
python3 -m json.tool catholic_readings_2026.json > /dev/null && echo "Valid JSON"
```

To check the number of days:

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
