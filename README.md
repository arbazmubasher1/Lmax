# EmoJournal

## Description
EmoJournal is a simple web application that helps users reflect on their day through journaling. When a user writes about their day, the app analyzes the text and responds with a one-line summary, the emotional tone of the entry, and a small piece of well-being advice. This project is built using Python and Flask, and it uses OpenAI’s language model to process the entries.

## Features
- Submit a journal entry using a simple web form
- Receive an AI-generated summary of the entry
- Detect the emotional tone of the text
- Get short advice or a positive suggestion
- View a history of your most recent journal logs

## Tech Stack
- Python 3
- Flask (backend + routing)
- OpenAI API (text analysis)
- SQLite (data storage)
- HTML/CSS with Bootstrap (frontend)
- Hosted on Azure using Ubuntu 24.04

## Folder Structure
```
emojournal/
├── app.py                  # Flask app logic
├── requirements.txt        # Python dependencies
├── templates/
│   └── index.html          # Frontend HTML template
├── static/
│   └── style.css           # Optional styling
```

## How to Run Locally
1. Clone or download the project folder.
2. Create a virtual environment and activate it.
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Set your OpenAI API key in the terminal:
   ```
   export OPENAI_API_KEY="your-key-here"
   ```
5. Run the app:
   ```
   export FLASK_APP=app.py
   flask run
   ```
6. Visit `http://localhost:5000` in your browser.

## How to Deploy on Azure
1. Create an Ubuntu 24.04 VM on Azure.
2. SSH into the VM using your `.pem` key.
3. Install Python, pip, and git:
   ```
   sudo apt update && sudo apt install python3-pip python3-venv git -y
   ```
4. Upload the project using `scp` or clone from GitHub.
5. Set up and activate a virtual environment:
   ```
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
6. Run the app on the public network:
   ```
   flask run --host=0.0.0.0
   ```
7. Make sure to open port 5000 in the Azure portal under Networking settings.

## Notes
- Be sure to keep your OpenAI API key secure.
- The application is currently running in development mode. For production, consider using Gunicorn and Nginx.
- This app is best suited for personal use or small demos.
