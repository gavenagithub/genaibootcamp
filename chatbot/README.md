# Professional AI Chatbot

A sleek, professional AI chatbot application built with Streamlit, featuring a clean interface and powerful AI capabilities.

## Features
- Professional and modern user interface
- Intelligent conversational responses
- Persistent conversation history
- Clean and minimalist design
- Customizable system prompt and settings
- Easy to set up and use

## Requirements
- Python 3.8+
- Streamlit
- Requests (for API calls)
- Python-dotenv

## Setup

1. Clone this repository
```bash
git clone <repository-url>
cd <repository-name>
```

2. Install the required packages
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the root directory with your API key
```
GOOGLE_API_KEY=your_api_key_here
```

You can get an API key from [Google AI Studio](https://aistudio.google.com/app/apikey).

## Running the Application

```bash
streamlit run app.py
```

The application will be available at `http://localhost:8501`.

## How to Use

1. Type your message in the input field at the bottom of the interface
2. Press Enter to send your message
3. The chatbot will respond to your query
4. Your conversation history is maintained during the session
5. Use the "Clear Conversation" button in the sidebar to start a new conversation

## Customizing the Chatbot

You can customize how the chatbot responds by using the Settings tab in the sidebar:

1. Click on the "Settings" tab in the sidebar
2. Modify the system prompt to change the chatbot's behavior and personality
3. Adjust the temperature slider to control the creativity of responses:
   - Lower values (closer to 0): More focused, deterministic responses
   - Higher values (closer to 1): More creative, varied responses
4. Click "Save Settings" to apply your changes

## API Implementation

This application uses the Google AI API in the backend, but the interface is designed to be generic and professional.

## Project Structure

```
project/
├── app.py                 # Main Streamlit application
├── functions.py           # Helper functions for API communication
├── .env                   # Environment file for API key (create this)
├── .streamlit/            # Streamlit configuration
│   └── config.toml        # Theme configuration
├── requirements.txt       # Project dependencies
└── README.md              # Documentation
```

## Customization

You can customize the appearance by modifying:
- The `.streamlit/config.toml` file for theme settings
- The CSS in `app.py` for more detailed styling

## License

MIT 