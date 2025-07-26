
from datetime import datetime
import os
import random
import requests
from dotenv import load_dotenv

# Load environment variables from .env file in the SAME directory
load_dotenv()  # Automatically looks for `.env` in the script's folder

BOT_ID = os.getenv("GROUPME_BOT_ID")
ACCESS_TOKEN = os.getenv("GROUPME_ACCESS_TOKEN")  # Required for image uploads
IMAGE_FOLDER = "birthday_images"  # Folder is in the same dir as script

def upload_image(image_path):
    """Uploads image to GroupMe and returns URL."""
    try:
        with open(image_path, 'rb') as img:
            headers = {'X-Access-Token': ACCESS_TOKEN}
            response = requests.post(
                'https://image.groupme.com/pictures',
                files={'file': (os.path.basename(image_path), img)},
                headers=headers
            )
            response.raise_for_status()  # Raises error if upload fails
            return response.json()['payload']['picture_url']
    except Exception as e:
        print(f"❌ Failed to upload image: {e}")
        return None

def send_message(text, image_url=None):
    """Sends message via GroupMe bot (with optional image)."""
    payload = {"bot_id": BOT_ID, "text": text}
    if image_url:
        payload["attachments"] = [{"type": "image", "url": image_url}]
    requests.post("https://api.groupme.com/v3/bots/post", json=payload)


def get_random_image():
    """Returns a RANDOM image path from IMAGE_FOLDER."""
    if not os.path.exists(IMAGE_FOLDER):
        print(f"❌ Folder '{IMAGE_FOLDER}' not found!")
        return None
        
    images = [
        f for f in os.listdir(IMAGE_FOLDER)
        if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))
    ]
    
    if not images:
        print(f"❌ No valid images in '{IMAGE_FOLDER}'.")
        return None
    
    # Shuffle the list to ensure randomness
    random.shuffle(images)  # <-- KEY FIX: Shuffle before picking
    return os.path.join(IMAGE_FOLDER, images[0])  # Pick first after shuffle

def check_birthdays():
    today = datetime.now().strftime("%m %d")
    names_today = []

    # Read birthdays.csv from the same directory
    with open("birthdays.csv", newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row["Month Day"].strip() == today:
                names_today.append(row["Name"])

    # Get a random image (if available)
    image_path = get_random_image()
    image_url = upload_image(image_path) if image_path else None

    # Send message
    if names_today:
        message = f"🎉 Happy Birthday {', '.join(names_today)}! 🎂"
    else:
        message = "No birthdays today! Enjoy your day! 🎉"
    
    send_message(message, image_url)

if __name__ == "__main__":
    print(f"Current working dir: {os.getcwd()}")  # Debug: Check where script runs
    check_birthdays()

