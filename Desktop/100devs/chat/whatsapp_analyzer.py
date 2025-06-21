import re
import csv
from collections import Counter
from datetime import datetime
import matplotlib.pyplot as plt

def startswithdateandtimeandriod(s):
    """Check if a line starts with date, time, and Android format"""
    pattern = r'^\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s[AP]M\s-\s(.+?):\s(.+)'
    result = re.match(pattern, s)
    return bool(result)

def findauthor(s):
    """Extract author name from a message line"""
    patterns = [
        r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s[AP]M\s-\s(.+?):\s(.+)',
        r'\[(\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}:\d{2}\]\s(.+?):\s(.+)'
    ]
    
    for pattern in patterns:
        result = re.match(pattern, s)
        if result:
            return result.group(1)
    return None

def getdatapoint(line):
    """Extract date, time, author, and message from a line"""
    splitline = line.split(' - ')
    dateTime = splitline[0]
    date, time = dateTime.split(', ')
    message = ' '.join(splitline[1:])
    
    if findauthor(message):
        splitmessage = message.split(': ')
        author = splitmessage[0]
        message = ' '.join(splitmessage[1:])
    else:
        author = None
    
    return date, time, author, message

def parse_whatsapp_chat(file_path):
    """Parse WhatsApp chat export file and return structured data"""
    parsedData = []
    conversation = open(file_path, 'r', encoding='utf-8')
    
    messageBuffer = []
    date, time, author = None, None, None
    
    while True:
        line = conversation.readline()
        if not line:
            break
        
        line = line.strip()
        if startswithdateandtimeandriod(line):
            if len(messageBuffer) > 0:
                parsedData.append([date, time, author, ' '.join(messageBuffer)])
            messageBuffer.clear()
            date, time, author, message = getdatapoint(line)
            messageBuffer.append(message)
        else:
            messageBuffer.append(line)
    
    conversation.close()
    return parsedData

def analyze_chat(parsed_data):
    """Perform comprehensive chat analysis"""
    
    # Basic statistics
    total_messages = len(parsed_data)
    
    # Messages per person
    authors = [row[2] for row in parsed_data if row[2]]
    messages_per_person = Counter(authors)
    total_participants = len(messages_per_person)
    
    # Most active hours
    hours = []
    for row in parsed_data:
        if row[1]:  # if time exists
            try:
                # Parse time like "2:30 PM"
                time_str = row[1]
                if 'PM' in time_str and not time_str.startswith('12'):
                    hour = int(time_str.split(':')[0]) + 12
                elif 'AM' in time_str and time_str.startswith('12'):
                    hour = 0
                else:
                    hour = int(time_str.split(':')[0])
                hours.append(hour)
            except:
                continue
    
    active_hours = Counter(hours)
    
    # Most active days
    days = []
    for row in parsed_data:
        if row[0]:  # if date exists
            try:
                # Parse date like "12/25/2023"
                date_str = row[0]
                date_obj = datetime.strptime(date_str, '%m/%d/%Y')
                day_name = date_obj.strftime('%A')
                days.append(day_name)
            except:
                continue
    
    active_days = Counter(days)
    
    # Word frequency
    all_words = ' '.join([row[3] for row in parsed_data if row[3]]).lower()
    words = re.findall(r'\b\w+\b', all_words)
    word_freq = Counter(words)
    
    return {
        'total_messages': total_messages,
        'total_participants': total_participants,
        'messages_per_person': messages_per_person,
        'active_hours': active_hours,
        'active_days': active_days,
        'word_freq': word_freq,
        'parsed_data': parsed_data
    }

def generate_report(analysis):
    """Generate a comprehensive chat analysis report"""
    print("=" * 50)
    print("WHATSAPP CHAT ANALYSIS REPORT")
    print("=" * 50)
    print(f"Total Messages: {analysis['total_messages']}")
    print(f"Total Participants: {analysis['total_participants']}")
    print()
    
    print("Top 5 Most Active Participants:")
    for i, (person, count) in enumerate(analysis['messages_per_person'].most_common(5), 1):
        print(f"{i}. {person}: {count} messages")
    print()
    
    print("Most Active Hours:")
    for hour, count in analysis['active_hours'].most_common(3):
        print(f"{hour}:00 - {count} messages")
    print()
    
    print("Most Active Days:")
    for day, count in analysis['active_days'].most_common(7):
        print(f"{day}: {count} messages")
    print()
    
    print("Top 10 Most Used Words:")
    for word, count in analysis['word_freq'].most_common(10):
        print(f"{word}: {count} times")

def create_visualizations(analysis):
    """Create various visualizations for the chat analysis"""
    
    # Create a figure with 4 subplots
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    
    # 1. Messages per person
    people = list(analysis['messages_per_person'].keys())[:10]
    counts = list(analysis['messages_per_person'].values())[:10]
    axes[0,0].bar(people, counts, color='skyblue')
    axes[0,0].set_title('Messages per Person', fontsize=14, fontweight='bold')
    axes[0,0].tick_params(axis='x', rotation=45)
    axes[0,0].set_ylabel('Number of Messages')
    
    # 2. Active hours
    hour_counts = [analysis['active_hours'].get(hour, 0) for hour in range(24)]
    axes[0,1].plot(range(24), hour_counts, marker='o', color='green', linewidth=2)
    axes[0,1].set_title('Most Active Hours', fontsize=14, fontweight='bold')
    axes[0,1].set_xlabel('Hour of Day')
    axes[0,1].set_ylabel('Number of Messages')
    axes[0,1].grid(True, alpha=0.3)
    
    # 3. Active days
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    day_counts = [analysis['active_days'].get(day, 0) for day in days]
    axes[1,0].bar(days, day_counts, color='orange')
    axes[1,0].set_title('Most Active Days', fontsize=14, fontweight='bold')
    axes[1,0].tick_params(axis='x', rotation=45)
    axes[1,0].set_ylabel('Number of Messages')
    
    # 4. Word frequency (top 10)
    top_words = dict(analysis['word_freq'].most_common(10))
    words = list(top_words.keys())
    counts = list(top_words.values())
    axes[1,1].bar(words, counts, color='red')
    axes[1,1].set_title('Top 10 Most Used Words', fontsize=14, fontweight='bold')
    axes[1,1].tick_params(axis='x', rotation=45)
    axes[1,1].set_ylabel('Frequency')
    
    plt.tight_layout()
    plt.savefig('whatsapp_analysis.png', dpi=300, bbox_inches='tight')
    plt.show()
    print("\n📊 Visualizations saved as 'whatsapp_analysis.png'")

def save_to_csv(analysis):
    """Save analysis data to CSV files"""
    
    # Save parsed data
    with open('chat_data.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Date', 'Time', 'Author', 'Message'])
        for row in analysis['parsed_data']:
            writer.writerow(row)
    
    # Save messages per person
    with open('messages_per_person.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Person', 'Message Count'])
        for person, count in analysis['messages_per_person'].most_common():
            writer.writerow([person, count])
    
    # Save word frequency
    with open('word_frequency.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Word', 'Frequency'])
        for word, count in analysis['word_freq'].most_common(50):
            writer.writerow([word, count])
    
    print("📁 Data saved to CSV files:")
    print("   - chat_data.csv")
    print("   - messages_per_person.csv")
    print("   - word_frequency.csv")

def main():
    """Main function to run the WhatsApp chat analyzer"""
    print("📱 WhatsApp Chat Analyzer")
    print("=" * 30)
    
    # Get file path from user
    file_path = input("Enter the path to your WhatsApp chat export (.txt file): ").strip()
    
    if not file_path.endswith('.txt'):
        print("❌ Please provide a .txt file")
        return
    
    try:
        print("\n🔄 Parsing WhatsApp chat...")
        parsed_data = parse_whatsapp_chat(file_path)
        
        print("📊 Analyzing chat data...")
        analysis = analyze_chat(parsed_data)
        
        print("\n" + "="*50)
        generate_report(analysis)
        
        # Ask user if they want visualizations
        show_viz = input("\nWould you like to see visualizations? (y/n): ").lower().strip()
        if show_viz == 'y':
            print("\n📈 Creating visualizations...")
            create_visualizations(analysis)
        
        # Ask user if they want to save data
        save_data = input("\nWould you like to save data to CSV files? (y/n): ").lower().strip()
        if save_data == 'y':
            print("\n💾 Saving data...")
            save_to_csv(analysis)
        
        print("\n✅ Analysis complete!")
        
    except FileNotFoundError:
        print(f"❌ File not found: {file_path}")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main() 