# WhatsApp Chat Analyzer - Local Version

A simple Python script to analyze WhatsApp chat exports locally.

## Features

- 📊 **Message Statistics**: Total messages and participants
- 🕐 **Time Analysis**: Most active hours and days
- 👥 **Participant Insights**: Who's most active
- 📈 **Visualizations**: Charts and graphs
- 💾 **Export Data**: Save results to CSV files

## How to Use

### 1. Export Your WhatsApp Chat

1. **Open WhatsApp** on your phone
2. **Go to the chat** you want to analyze
3. **Tap the three dots** (⋮) in the top right
4. **Select "More"** → **"Export chat"**
5. **Choose "Without media"** (faster and smaller)
6. **Save the .txt file** to your computer

### 2. Run the Analyzer

```bash
python whatsapp_analyzer.py
```

### 3. Follow the Prompts

- Enter the path to your chat file
- Choose whether to see visualizations
- Choose whether to save data to CSV

## Requirements

```bash
pip install matplotlib
```

## Output Files

- `whatsapp_analysis.png` - Visualizations
- `chat_data.csv` - All parsed messages
- `messages_per_person.csv` - Message counts per person
- `word_frequency.csv` - Most used words

## Example Output

```
==================================================
WHATSAPP CHAT ANALYSIS REPORT
==================================================
Total Messages: 1250
Total Participants: 5

Top 5 Most Active Participants:
1. John: 450 messages
2. Sarah: 320 messages
3. Mike: 280 messages
4. Lisa: 150 messages
5. Alex: 50 messages

Most Active Hours:
14:00 - 180 messages
20:00 - 150 messages
22:00 - 120 messages

Most Active Days:
Saturday: 200 messages
Friday: 180 messages
Sunday: 160 messages
Monday: 140 messages
Tuesday: 120 messages
Wednesday: 100 messages
Thursday: 80 messages

Top 10 Most Used Words:
hello: 45 times
thanks: 40 times
okay: 35 times
good: 30 times
...
```

## Privacy

- **No data is sent anywhere** - everything runs locally
- **Your chat data stays private** on your computer
- **No internet connection required**

## Support

If you encounter any issues:
1. Make sure your chat export is in .txt format
2. Check that the file path is correct
3. Ensure matplotlib is installed

---

**Happy analyzing! 📱📊** 