# Catholic Quiz Questions (2025-2026)

## Overview
This JSON file contains Catholic quiz questions for every day from January 1, 2025 to December 31, 2026.

## File Details
- **Filename**: `catholic_quizzes_2025_2026.json`
- **Total Days**: 730 days
- **Questions per Day**: 5
- **Total Questions**: 3,650

## JSON Structure

```json
{
  "title": "Catholic Daily Quiz Questions",
  "description": "Daily Catholic quiz questions based on Catholic teachings, Scripture, Saints, and Church tradition",
  "period": {
    "start_date": "2025-01-01",
    "end_date": "2026-12-31",
    "total_days": 730
  },
  "questions_per_day": 5,
  "total_questions": 3650,
  "quizzes": [
    {
      "date": "2025-01-01",
      "day_of_week": "Wednesday",
      "questions": [
        {
          "question_number": 1,
          "question": "Who wrote the Gospel of John?",
          "options": ["St. Peter", "St. John the Apostle", "St. Paul", "St. Matthew"],
          "correct_answer": "St. John the Apostle",
          "category": "Scripture"
        },
        // ... 4 more questions
      ]
    },
    // ... 729 more days
  ]
}
```

## Question Categories

The quiz questions are organized into the following categories:

1. **Scripture** - Questions about the Bible, Gospels, and biblical stories
2. **Sacraments** - Questions about the seven sacraments of the Catholic Church
3. **Saints** - Questions about Catholic saints and holy figures
4. **Liturgy** - Questions about Catholic worship, seasons, and ceremonies
5. **Church** - Questions about Catholic Church structure and organization
6. **Jesus** - Questions about the life and teachings of Jesus Christ
7. **Mary** - Questions about the Blessed Virgin Mary
8. **Prayer** - Questions about Catholic prayers and devotions
9. **Commandments** - Questions about the Ten Commandments
10. **Doctrine** - Questions about Catholic theological teachings
11. **Church Teaching** - Questions about the Magisterium and Catechism
12. **Virtues** - Questions about theological and cardinal virtues

## Usage in Android App

### Loading the JSON File

```kotlin
// In your Activity or Fragment
fun loadQuizQuestions(context: Context): QuizData? {
    return try {
        val jsonString = context.assets.open("catholic_quizzes_2025_2026.json")
            .bufferedReader()
            .use { it.readText() }
        
        val gson = Gson()
        gson.fromJson(jsonString, QuizData::class.java)
    } catch (e: Exception) {
        e.printStackTrace()
        null
    }
}
```

### Data Classes

```kotlin
data class QuizData(
    val title: String,
    val description: String,
    val period: Period,
    val questions_per_day: Int,
    val total_questions: Int,
    val quizzes: List<DailyQuiz>
)

data class Period(
    val start_date: String,
    val end_date: String,
    val total_days: Int
)

data class DailyQuiz(
    val date: String,
    val day_of_week: String,
    val questions: List<Question>
)

data class Question(
    val question_number: Int,
    val question: String,
    val options: List<String>,
    val correct_answer: String,
    val category: String
)
```

### Getting Quiz for Today

```kotlin
fun getQuizForDate(quizData: QuizData, date: String): DailyQuiz? {
    return quizData.quizzes.find { it.date == date }
}

// Usage
val todayDate = SimpleDateFormat("yyyy-MM-dd", Locale.getDefault()).format(Date())
val todayQuiz = getQuizForDate(quizData, todayDate)
```

### Getting Quiz by Index

```kotlin
fun getQuizByDayNumber(quizData: QuizData, dayNumber: Int): DailyQuiz? {
    return if (dayNumber in 0 until quizData.quizzes.size) {
        quizData.quizzes[dayNumber]
    } else null
}
```

## Example Questions

Here are some example questions from the quiz:

**Scripture Category:**
- Q: Who wrote the Gospel of John?
- A: St. John the Apostle

**Sacraments Category:**
- Q: How many sacraments are there in the Catholic Church?
- A: 7

**Saints Category:**
- Q: Who is the patron saint of animals?
- A: St. Francis of Assisi

**Liturgy Category:**
- Q: What is the color worn during Advent and Lent?
- A: Purple

**Jesus Category:**
- Q: Where was Jesus born?
- A: Bethlehem

## Notes

- All questions are based on traditional Catholic teachings and Scripture
- Each question has exactly 4 multiple choice options
- The correct answer is clearly identified in the `correct_answer` field
- Questions cycle through different categories to provide variety
- The file size is approximately 1.3 MB

## Contributing

To add more questions or modify existing ones, edit the source generation script and regenerate the JSON file.

## License

This quiz content is provided for educational and religious purposes.
