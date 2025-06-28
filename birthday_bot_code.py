import csv
import os
import requests
from datetime import datetime
from apscheduler.schedulers.blocking import BlockingScheduler
from dotenv import load_dotenv

print("✅ Birthday bot is running...", flush=True)
# Load environment variables (from Replit "Secrets" or a .env file if local)
load_dotenv()

# Get credentials from environment variables
BOT_ID = os.getenv("GROUPME_BOT_ID")
IMAGE_TOKEN = os.getenv("GROUPME_IMAGE_TOKEN")


# Function to send a message to GroupMe
def send_message(text, image_url=None):
    message_data = {
        "bot_id": BOT_ID,
        "text": text,
    }
    if image_url:
        message_data["attachments"] = [{
            "type": "image",
            "url": image_url
        }]
    requests.post("https://api.groupme.com/v3/bots/post", json=message_data)


# Function to upload image to GroupMe (optional)
def upload_image(image_path):
    headers = {"X-Access-Token": IMAGE_TOKEN}
    with open(image_path, "rb") as img:
        response = requests.post(
            "https://image.groupme.com/pictures",
            headers=headers,
            files={"file": img}
        )
    if response.status_code == 200:
        return response.json()["payload"]["picture_url"]
    else:
        print("❌ Image upload failed:", response.text)
        return None

# Function to check if today is anyone's birthday
def check_birthdays():
    today = datetime.now().strftime("%m %d")  # Format: 06 24
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
        # Upload image once
        image_url = upload_image("birthday_image.jpg")
        print("✅ Uploaded Image URL:", image_url)

        names_str = ", ".join(names_today)
        message = f"🎉 Happy Birthday {names_str}! 🎂"

        # Send message with image if upload successful
        if image_url:
            send_message(message, image_url)
        else:
            send_message(message)
    else:
        print("⚠️ No birthdays matched today.")


# Set up the scheduler
# Set up the scheduler or run manually
# Run the birthday check manually
if __name__ == "__main__":
    print("🚀 Running birthday check manually...")
    check_birthdays()


