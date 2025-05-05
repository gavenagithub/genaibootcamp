import os
import requests
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Base URL for API
API_BASE_URL = "https://generativelanguage.googleapis.com/v1beta/models"
MODEL_NAME = "gemini-2.0-flash"

# Get API key
def get_api_key():
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY not found in environment variables")
    return api_key

# Function to get response from AI model
def get_gemini_response(user_input, chat_history=None, system_prompt=None, temperature=0.7):
    api_key = get_api_key()
    url = f"{API_BASE_URL}/{MODEL_NAME}:generateContent?key={api_key}"
    
    headers = {
        "Content-Type": "application/json"
    }
    
    # If we have chat history, include it in the request
    contents = []
    
    # Add system prompt if provided
    if system_prompt:
        contents.append({
            "role": "system",
            "parts": [{"text": system_prompt}]
        })
    
    if chat_history:
        for message in chat_history:
            role = "user" if message.get("role") == "user" else "model"
            contents.append({
                "role": role,
                "parts": [{"text": message.get("content", "")}]
            })
    
    # Add the current user message
    contents.append({
        "role": "user",
        "parts": [{"text": user_input}]
    })
    
    data = {
        "contents": contents if contents else [{
            "parts": [{"text": user_input}]
        }],
        "generationConfig": {
            "temperature": float(temperature)
        }
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()  # Raise an exception for HTTP errors
        
        response_json = response.json()
        
        # Extract the response text
        if "candidates" in response_json and len(response_json["candidates"]) > 0:
            candidate = response_json["candidates"][0]
            if "content" in candidate and "parts" in candidate["content"]:
                text = candidate["content"]["parts"][0]["text"]
                
                # Update chat history
                if chat_history is None:
                    chat_history = []
                
                # Add user message to history
                chat_history.append({"role": "user", "content": user_input})
                
                # Add assistant response to history
                chat_history.append({"role": "model", "content": text})
                
                return text, chat_history
        
        # If we couldn't extract the text using the expected structure
        return "I couldn't generate a response. Please try again.", chat_history or []
    
    except Exception as e:
        print(f"Error: {e}")
        return f"An error occurred: {str(e)}", chat_history or []

# Function to map roles between model and Streamlit
def map_role(role):
    if role == "model":
        return "assistant"
    else:
        return role 