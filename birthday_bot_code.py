import csv
from datetime import datetime
import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(dotenv_path="/Users/elii/Desktop/secretary_committee/.env")

BOT_ID = os.getenv("GROUPME_BOT_ID")

def send_message(text):
    requests.post("https://api.groupme.com/v3/bots/post", json={
        "bot_id": BOT_ID,
        "text": text
    })

def check_birthdays():
    today = datetime.now().strftime("%m %d")  # Format: 06 23
    print("🔎 Today is:", today)
    names_today = []

    with open("birthdays.csv", newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        for i, row in enumerate(reader):
            month_day = row["Month Day"].strip()
            print(f"Row {i+1} → {row['Name']} has birthday on {month_day}")
            if month_day == today:
                print(f" ✅ Match: {row['Name']}")
                names_today.append(row["Name"])

    if names_today:
        names_str = ", ".join(names_today)
        message = f"🎉 Happy Birthday {names_str}! 🎂"
        send_message(message)
    else:
        print("⚠️ No birthdays matched today.")

if __name__ == "__main__":
    check_birthdays()



