# GroupMe Birthday Bot 🎉

This is a simple Python bot that automatically sends birthday messages to a GroupMe group using the GroupMe Bot API. It reads a `birthdays.csv` file and checks for any birthdays matching today’s date. If a match is found, it sends a celebratory message to the group.

## Features

- ✅ Daily check for birthdays via cron job
- ✅ GroupMe API integration using a bot ID from `.env`
- ✅ Reads birthday data from a `.csv` file
- ✅ Easily customizable

## Setup

1. Clone this repo:
   ```bash
   git clone https://github.com/elii-lopez/groupme_birthday_bot.git
   cd groupme_birthday_bot

    Install dependencies:

pip install -r requirements.txt

Create a .env file:

GROUPME_BOT_ID=your_bot_id_here

Make sure your birthdays.csv file has this format:

Name,Month Day
John Doe,06 23
Jane Smith,12 01

Schedule it with cron:

    * * * * * cd /path/to/folder && /usr/bin/python3 birthday_bot_code.py

Connect with Me or Ask a Question:

🔗 LinkedIn – [Elii Lopez](https://www.linkedin.com/in/elii-lopez-b41021298/)
