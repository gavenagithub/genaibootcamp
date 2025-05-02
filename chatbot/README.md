# Gemini Chatbot

A Python web-based chatbot application that uses Google's Gemini 2.0 model.

## Requirements

- Python 3.7+
- Required packages (listed in requirements.txt)

## Setup

1. Clone this repository
2. Install the requirements:
   ```
   pip install -r requirements.txt
   ```
3. The API key is already included in the code, but you can modify it in `chatbot.py` if needed

## Usage

Run the application:
```
python chatbot.py
```

Then open your web browser and navigate to:
```
http://127.0.0.1:5000
```

The chatbot interface will open in your browser:
- Type your messages in the text box at the bottom
- Press Enter or click the "Send" button to send your message
- The chatbot will respond using the Gemini 2.0 model

## Features

- Modern web-based UI using HTML/CSS
- Chat history maintained during the session
- Asynchronous message processing
- Error handling for API issues 