#!/usr/bin/env python3
"""
Catholic Daily Readings Generator for 2026 with Sample Data

This script generates a complete JSON file for 2026 with sample Catholic readings.
It includes actual readings for major liturgical dates and placeholder text for others.

NOTE: Full 2026 data is not yet available from USCCB. This generates a working
JSON file with:
- Actual readings for major feast days (embedded in script)
- Placeholders for regular days (to be updated when USCCB publishes 2026 data)

Usage:
    python3 generate_readings_with_sample_data.py [year] [output_path]
"""

import json
import sys
from datetime import date, timedelta
from typing import Dict, List, Any

# Sample actual Catholic readings for major feast days
# These are from the New American Bible, Revised Edition (NABRE)
MAJOR_FEAST_READINGS = {
    "01-01": {  # Solemnity of Mary, Mother of God
        "title": "Solemnity of Mary, the Holy Mother of God",
        "readings": [
            {
                "type": "First Reading",
                "citation": "Numbers 6:22-27",
                "text": "The LORD said to Moses: Speak to Aaron and his sons and tell them: This is how you shall bless the Israelites. Say to them: The LORD bless you and keep you! The LORD let his face shine upon you, and be gracious to you! The LORD look upon you kindly and give you peace! So shall they invoke my name upon the Israelites, and I will bless them."
            },
            {
                "type": "Psalm",
                "citation": "Psalm 67:2-3, 5, 6, 8",
                "text": "R. May God bless us in his mercy.\nMay God have pity on us and bless us;\nmay he let his face shine upon us.\nSo may your way be known upon earth;\namong all nations, your salvation.\nR. May God bless us in his mercy.\nMay the nations be glad and exult\nbecause you rule the peoples in equity;\nthe nations on the earth you guide.\nR. May God bless us in his mercy.\nMay the peoples praise you, O God;\nmay all the peoples praise you!\nMay God bless us,\nand may all the ends of the earth fear him!\nR. May God bless us in his mercy."
            },
            {
                "type": "Second Reading",
                "citation": "Galatians 4:4-7",
                "text": "Brothers and sisters: When the fullness of time had come, God sent his Son, born of a woman, born under the law, to ransom those under the law, so that we might receive adoption as sons. As proof that you are sons, God sent the Spirit of his Son into our hearts, crying out, \"Abba, Father!\" So you are no longer a slave but a son, and if a son then also an heir, through God."
            },
            {
                "type": "Gospel",
                "citation": "Luke 2:16-21",
                "text": "The shepherds went in haste to Bethlehem and found Mary and Joseph, and the infant lying in the manger. When they saw this, they made known the message that had been told them about this child. All who heard it were amazed by what had been told them by the shepherds. And Mary kept all these things, reflecting on them in her heart. Then the shepherds returned, glorifying and praising God for all they had heard and seen, just as it had been told to them. When eight days were completed for his circumcision, he was named Jesus, the name given him by the angel before he was conceived in the womb."
            }
        ]
    },
    "01-06": {  # Epiphany of the Lord
        "title": "The Epiphany of the Lord",
        "readings": [
            {
                "type": "First Reading",
                "citation": "Isaiah 60:1-6",
                "text": "Rise up in splendor, Jerusalem! Your light has come, the glory of the Lord shines upon you. See, darkness covers the earth, and thick clouds cover the peoples; but upon you the LORD shines, and over you appears his glory. Nations shall walk by your light, and kings by your shining radiance. Raise your eyes and look about; they all gather and come to you: your sons come from afar, and your daughters in the arms of their nurses. Then you shall be radiant at what you see, your heart shall throb and overflow, for the riches of the sea shall be emptied out before you, the wealth of nations shall be brought to you. Caravans of camels shall fill you, dromedaries from Midian and Ephah; all from Sheba shall come bearing gold and frankincense, and proclaiming the praises of the LORD."
            },
            {
                "type": "Psalm",
                "citation": "Psalm 72:1-2, 7-8, 10-11, 12-13",
                "text": "R. Lord, every nation on earth will adore you.\nO God, with your judgment endow the king,\nand with your justice, the king's son;\nhe shall govern your people with justice\nand your afflicted ones with judgment.\nR. Lord, every nation on earth will adore you.\nJustice shall flower in his days,\nand profound peace, till the moon be no more.\nMay he rule from sea to sea,\nand from the River to the ends of the earth.\nR. Lord, every nation on earth will adore you.\nThe kings of Tarshish and the Isles shall offer gifts;\nthe kings of Arabia and Seba shall bring tribute.\nAll kings shall pay him homage,\nall nations shall serve him.\nR. Lord, every nation on earth will adore you.\nFor he shall rescue the poor when he cries out,\nand the afflicted when he has no one to help him.\nHe shall have pity for the lowly and the poor;\nthe lives of the poor he shall save.\nR. Lord, every nation on earth will adore you."
            },
            {
                "type": "Second Reading",
                "citation": "Ephesians 3:2-3a, 5-6",
                "text": "Brothers and sisters: You have heard of the stewardship of God's grace that was given to me for your benefit, namely, that the mystery was made known to me by revelation. It was not made known to people in other generations as it has now been revealed to his holy apostles and prophets by the Spirit: that the Gentiles are coheirs, members of the same body, and copartners in the promise in Christ Jesus through the gospel."
            },
            {
                "type": "Gospel",
                "citation": "Matthew 2:1-12",
                "text": "When Jesus was born in Bethlehem of Judea, in the days of King Herod, behold, magi from the east arrived in Jerusalem, saying, \"Where is the newborn king of the Jews? We saw his star at its rising and have come to do him homage.\" When King Herod heard this, he was greatly troubled, and all Jerusalem with him. Assembling all the chief priests and the scribes of the people, he inquired of them where the Christ was to be born. They said to him, \"In Bethlehem of Judea, for thus it has been written through the prophet: And you, Bethlehem, land of Judah, are by no means least among the rulers of Judah; since from you shall come a ruler, who is to shepherd my people Israel.\" Then Herod called the magi secretly and ascertained from them the time of the star's appearance. He sent them to Bethlehem and said, \"Go and search diligently for the child. When you have found him, bring me word, that I too may go and do him homage.\" After their audience with the king they set out. And behold, the star that they had seen at its rising preceded them, until it came and stopped over the place where the child was. They were overjoyed at seeing the star, and on entering the house they saw the child with Mary his mother. They prostrated themselves and did him homage. Then they opened their treasures and offered him gifts of gold, frankincense, and myrrh. And having been warned in a dream not to return to Herod, they departed for their country by another way."
            }
        ]
    },
    "12-25": {  # Christmas
        "title": "The Nativity of the Lord (Christmas)",
        "readings": [
            {
                "type": "First Reading",
                "citation": "Isaiah 52:7-10",
                "text": "How beautiful upon the mountains are the feet of him who brings glad tidings, announcing peace, bearing good news, announcing salvation, and saying to Zion, \"Your God is King!\" Hark! Your sentinels raise a cry, together they shout for joy, for they see directly, before their eyes, the LORD restoring Zion. Break out together in song, O ruins of Jerusalem! For the LORD comforts his people, he redeems Jerusalem. The LORD has bared his holy arm in the sight of all the nations; all the ends of the earth will behold the salvation of our God."
            },
            {
                "type": "Psalm",
                "citation": "Psalm 98:1, 2-3, 3-4, 5-6",
                "text": "R. All the ends of the earth have seen the saving power of God.\nSing to the LORD a new song,\nfor he has done wondrous deeds;\nhis right hand has won victory for him,\nhis holy arm.\nR. All the ends of the earth have seen the saving power of God.\nThe LORD has made his salvation known:\nin the sight of the nations he has revealed his justice.\nHe has remembered his kindness and his faithfulness\ntoward the house of Israel.\nR. All the ends of the earth have seen the saving power of God.\nAll the ends of the earth have seen\nthe salvation by our God.\nSing joyfully to the LORD, all you lands;\nbreak into song; sing praise.\nR. All the ends of the earth have seen the saving power of God.\nSing praise to the LORD with the harp,\nwith the harp and melodious song.\nWith trumpets and the sound of the horn\nsing joyfully before the King, the LORD.\nR. All the ends of the earth have seen the saving power of God."
            },
            {
                "type": "Second Reading",
                "citation": "Hebrews 1:1-6",
                "text": "Brothers and sisters: In times past, God spoke in partial and various ways to our ancestors through the prophets; in these last days, he has spoken to us through the Son, whom he made heir of all things and through whom he created the universe, who is the refulgence of his glory, the very imprint of his being, and who sustains all things by his mighty word. When he had accomplished purification from sins, he took his seat at the right hand of the Majesty on high, as far superior to the angels as the name he has inherited is more excellent than theirs. For to which of the angels did God ever say: You are my son; this day I have begotten you? Or again: I will be a father to him, and he shall be a son to me? And again, when he leads the firstborn into the world, he says: Let all the angels of God worship him."
            },
            {
                "type": "Gospel",
                "citation": "John 1:1-18",
                "text": "In the beginning was the Word, and the Word was with God, and the Word was God. He was in the beginning with God. All things came to be through him, and without him nothing came to be. What came to be through him was life, and this life was the light of the human race; the light shines in the darkness, and the darkness has not overcome it. A man named John was sent from God. He came for testimony, to testify to the light, so that all might believe through him. He was not the light, but came to testify to the light. The true light, which enlightens everyone, was coming into the world. He was in the world, and the world came to be through him, but the world did not know him. He came to what was his own, but his own people did not accept him. But to those who did accept him he gave power to become children of God, to those who believe in his name, who were born not by natural generation nor by human choice nor by a man's decision but of God. And the Word became flesh and made his dwelling among us, and we saw his glory, the glory as of the Father's only Son, full of grace and truth. John testified to him and cried out, saying, \"This was he of whom I said, 'The one who is coming after me ranks ahead of me because he existed before me.'\" From his fullness we have all received, grace in place of grace, because while the law was given through Moses, grace and truth came through Jesus Christ. No one has ever seen God. The only Son, God, who is at the Father's side, has revealed him."
            }
        ]
    }
}


def get_liturgical_title(target_date: date) -> str:
    """Get the liturgical title for a given date."""
    month_day = target_date.strftime("%m-%d")
    
    # Check if we have data for this date
    if month_day in MAJOR_FEAST_READINGS:
        return MAJOR_FEAST_READINGS[month_day]["title"]
    
    # Other known feast days
    special_days = {
        "12-08": "The Immaculate Conception of the Blessed Virgin Mary",
        "11-01": "All Saints",
        "11-02": "The Commemoration of All the Faithful Departed (All Souls' Day)",
        "12-24": "Christmas Eve",
        "12-26": "Saint Stephen, The First Martyr",
        "12-27": "Saint John, Apostle and Evangelist",
        "12-28": "The Holy Innocents, Martyrs",
    }
    
    if month_day in special_days:
        return special_days[month_day]
    
    # Default weekday naming
    weekday = target_date.strftime("%A")
    return f"Daily Reading - {weekday}"


def generate_reading_for_date(target_date: date) -> Dict[str, Any]:
    """Generate reading entry for a specific date."""
    date_str = target_date.strftime("%Y-%m-%d")
    month_day = target_date.strftime("%m-%d")
    
    # Check if we have full data for this date
    if month_day in MAJOR_FEAST_READINGS:
        reading_data = MAJOR_FEAST_READINGS[month_day].copy()
        reading_data["date"] = date_str
        return reading_data
    
    # Otherwise, create placeholder with liturgical title
    title = get_liturgical_title(target_date)
    
    return {
        "date": date_str,
        "title": title,
        "readings": [
            {
                "type": "First Reading",
                "citation": "To be updated from USCCB",
                "text": f"This reading will be available from USCCB closer to {date_str}. To get actual readings, regenerate this file in late 2025 or early 2026 using the generator script with internet access."
            },
            {
                "type": "Psalm",
                "citation": "To be updated from USCCB",
                "text": "Psalm content will be available from USCCB as the date approaches."
            },
            {
                "type": "Gospel",
                "citation": "To be updated from USCCB",
                "text": "Gospel reading will be available from USCCB as the date approaches."
            }
        ]
    }


def generate_all_readings(year: int) -> List[Dict[str, Any]]:
    """Generate readings for all days in the specified year."""
    readings = []
    start_date = date(year, 1, 1)
    end_date = date(year, 12, 31)
    
    current_date = start_date
    day_count = 0
    
    print(f"Generating Catholic readings for {year}...")
    print(f"From {start_date} to {end_date}")
    print()
    print("NOTE: This generator includes actual readings for major feast days")
    print("      and placeholders for regular days (USCCB has not published")
    print("      full 2026 data yet).")
    print()
    
    while current_date <= end_date:
        day_count += 1
        
        if day_count % 30 == 0 or day_count == 1:
            print(f"Processing day {day_count}/365: {current_date}")
        
        reading = generate_reading_for_date(current_date)
        readings.append(reading)
        
        current_date += timedelta(days=1)
    
    print(f"\nCompleted! Generated {len(readings)} daily readings.")
    return readings


def save_to_json(readings: List[Dict[str, Any]], output_path: str) -> None:
    """Save the readings to a JSON file."""
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(readings, f, indent=2, ensure_ascii=False)
    
    print(f"\nJSON file saved to: {output_path}")
    file_size = len(json.dumps(readings))
    print(f"File size: {file_size:,} bytes ({file_size/1024:.1f} KB)")


def main():
    """Main entry point."""
    print("=" * 70)
    print("Catholic Daily Readings Generator for 2026")
    print("=" * 70)
    print()
    print("COPYRIGHT AND USAGE NOTES:")
    print("-" * 70)
    print("Scripture texts are from the New American Bible, Revised Edition")
    print("(NABRE) © 2010, 1991, 1986, 1970 Confraternity of Christian")
    print("Doctrine, Washington, D.C.")
    print()
    print("For use in mobile apps:")
    print("• Personal, educational, and religious use is permitted")
    print("• For commercial use, contact USCCB for licensing")
    print("• Always provide proper attribution in your app")
    print()
    print("Source: USCCB (United States Conference of Catholic Bishops)")
    print("=" * 70)
    print()
    
    # Parse command line arguments
    year = 2026
    output_path = "GithubUsers/app/src/main/assets/catholic_readings_2026.json"
    
    if len(sys.argv) > 1:
        try:
            year = int(sys.argv[1])
        except ValueError:
            print(f"Warning: Invalid year '{sys.argv[1]}', using default 2026")
    
    if len(sys.argv) > 2:
        output_path = sys.argv[2]
    
    # Generate readings
    readings = generate_all_readings(year)
    
    # Save to file
    save_to_json(readings, output_path)
    
    print()
    print("SUCCESS! The readings JSON file has been generated.")
    print()
    print("✓ Includes actual readings for major feast days:")
    print("  - January 1: Solemnity of Mary, Mother of God")
    print("  - January 6: Epiphany of the Lord")
    print("  - December 25: Nativity of the Lord (Christmas)")
    print()
    print("ℹ Other dates have placeholder text with instructions to update")
    print("  when USCCB publishes complete 2026 readings.")
    print()
    print("Next steps:")
    print("1. Use the generated JSON file in your Android app now")
    print("2. Regenerate in late 2025/early 2026 for complete data")
    print("3. See CATHOLIC_READINGS_README.md for Android integration code")


if __name__ == "__main__":
    main()
