import google.generativeai as genai
from flask import Flask, render_template, request, jsonify
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure the API
API_KEY = "AIzaSyAjFEfQWHqUXSOJ8kdvBbhaObc2dw2VKNk"
genai.configure(api_key=API_KEY)

# Set the model to Gemini 2.0
model = genai.GenerativeModel('gemini-2.0-flash')

app = Flask(__name__)

# Create templates directory if it doesn't exist
os.makedirs('templates', exist_ok=True)
os.makedirs('static', exist_ok=True)

# Create chat history
chat_history = []

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/send_message', methods=['POST'])
def send_message():
    user_message = request.json.get('message', '')
    
    if not user_message.strip():
        return jsonify({'error': 'Empty message'})
    
    # Append user message to chat history
    if len(chat_history) > 0:
        # Format the chat history for Gemini API
        formatted_history = []
        for entry in chat_history:
            formatted_history.append({"role": entry["role"], "parts": [entry["content"]]})
        
        # Create a chat session with history
        chat = model.start_chat(history=formatted_history)
        
        # Send the message and get response
        try:
            response = chat.send_message(user_message)
            bot_response = response.text
        except Exception as e:
            bot_response = f"An error occurred: {str(e)}"
    else:
        # First message, no history yet
        try:
            response = model.generate_content(user_message)
            bot_response = response.text
        except Exception as e:
            bot_response = f"An error occurred: {str(e)}"
    
    # Append messages to history
    chat_history.append({"role": "user", "content": user_message})
    chat_history.append({"role": "model", "content": bot_response})
    
    # Keep only the last 10 messages to avoid context length issues
    while len(chat_history) > 20:
        chat_history.pop(0)
    
    return jsonify({
        'user_message': user_message,
        'bot_response': bot_response
    })

if __name__ == '__main__':
    # Create the index.html file
    with open('templates/index.html', 'w') as f:
        f.write('''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Gemini Chatbot</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .chat-container {
            display: flex;
            flex-direction: column;
            height: 70vh;
            border: 1px solid #ddd;
            border-radius: 8px;
            background-color: #fff;
            overflow: hidden;
        }
        .chat-messages {
            flex: 1;
            overflow-y: auto;
            padding: 20px;
        }
        .input-container {
            display: flex;
            padding: 10px;
            border-top: 1px solid #ddd;
            background-color: #f9f9f9;
        }
        #message-input {
            flex: 1;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 4px;
            margin-right: 10px;
        }
        #send-button {
            padding: 10px 20px;
            background-color: #4285f4;
            color: white;
            border: none;
            border-radius: 4px;
            cursor: pointer;
        }
        #send-button:hover {
            background-color: #3367d6;
        }
        .message {
            margin-bottom: 15px;
            padding: 10px 15px;
            border-radius: 18px;
            max-width: 70%;
            word-wrap: break-word;
        }
        .user-message {
            background-color: #e3f2fd;
            margin-left: auto;
            border-bottom-right-radius: 4px;
        }
        .bot-message {
            background-color: #f1f1f1;
            margin-right: auto;
            border-bottom-left-radius: 4px;
        }
        .typing-indicator {
            display: none;
            color: #888;
            font-style: italic;
            margin-bottom: 10px;
        }
        h1 {
            text-align: center;
            color: #4285f4;
        }
    </style>
</head>
<body>
    <h1>Gemini 2.5 Chatbot</h1>
    <div class="chat-container">
        <div class="chat-messages" id="chat-messages">
            <div class="message bot-message">Hello! I'm your Gemini-powered assistant. How can I help you today?</div>
            <div class="typing-indicator" id="typing-indicator">Gemini is thinking...</div>
        </div>
        <div class="input-container">
            <input type="text" id="message-input" placeholder="Type your message here..." autofocus>
            <button id="send-button">Send</button>
        </div>
    </div>

    <script>
        document.addEventListener('DOMContentLoaded', function() {
            const messageInput = document.getElementById('message-input');
            const sendButton = document.getElementById('send-button');
            const chatMessages = document.getElementById('chat-messages');
            const typingIndicator = document.getElementById('typing-indicator');

            // Send message when Send button is clicked
            sendButton.addEventListener('click', sendMessage);

            // Send message when Enter key is pressed
            messageInput.addEventListener('keypress', function(e) {
                if (e.key === 'Enter') {
                    sendMessage();
                }
            });

            function sendMessage() {
                const message = messageInput.value.trim();
                if (!message) return;

                // Add user message to chat
                appendMessage(message, 'user');
                messageInput.value = '';

                // Show typing indicator
                typingIndicator.style.display = 'block';
                
                // Disable input and button while waiting for response
                messageInput.disabled = true;
                sendButton.disabled = true;

                // Send message to server
                fetch('/send_message', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ message: message }),
                })
                .then(response => response.json())
                .then(data => {
                    // Hide typing indicator
                    typingIndicator.style.display = 'none';
                    
                    // Add bot message to chat
                    appendMessage(data.bot_response, 'bot');
                    
                    // Re-enable input and button
                    messageInput.disabled = false;
                    sendButton.disabled = false;
                    messageInput.focus();
                })
                .catch(error => {
                    console.error('Error:', error);
                    typingIndicator.style.display = 'none';
                    appendMessage('Sorry, an error occurred. Please try again.', 'bot');
                    messageInput.disabled = false;
                    sendButton.disabled = false;
                });
            }

            function appendMessage(content, sender) {
                const messageElement = document.createElement('div');
                messageElement.classList.add('message');
                messageElement.classList.add(sender + '-message');
                messageElement.textContent = content;
                
                chatMessages.appendChild(messageElement);
                
                // Scroll to bottom
                chatMessages.scrollTop = chatMessages.scrollHeight;
            }
        });
    </script>
</body>
</html>
''')
    
    # Create a simple CSS file
    with open('static/style.css', 'w') as f:
        f.write('''
/* Additional styles can be added here */
''')
    
    # Run the app
    app.run(debug=True) 