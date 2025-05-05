import streamlit as st
import os
from dotenv import load_dotenv
from functions import get_gemini_response, map_role

# Load environment variables
load_dotenv()

# Initialize session state for settings
if "system_prompt" not in st.session_state:
    st.session_state.system_prompt = "You are a helpful, intelligent chatbot that provides informative and concise responses."

if "temperature" not in st.session_state:
    st.session_state.temperature = 0.7

if "sidebar_tab" not in st.session_state:
    st.session_state.sidebar_tab = "About"

# Configure Streamlit page
st.set_page_config(
    page_title="AI Chatbot",
    page_icon="💬",
    layout="wide"
)

# Custom CSS for a professional UI
st.markdown("""
<style>
    /* General styling */
    .main {
        background-color: #FFFFFF;
        color: #333333;
        font-family: 'Helvetica Neue', Arial, sans-serif;
        padding: 1rem;
        max-width: 1200px;
        margin: 0 auto;
    }
    
    /* Input field styling */
    .stTextInput > div > div > input {
        background-color: #F8F9FA;
        border: 1px solid #E0E0E0;
        border-radius: 8px;
        padding: 10px;
        font-size: 16px;
    }
    
    /* Button styling */
    .stButton>button {
        background-color: #2E86C1;
        color: white;
        border: none;
        border-radius: 6px;
        padding: 0.5rem 1rem;
        font-weight: 500;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        transition: all 0.2s ease;
    }
    .stButton>button:hover {
        background-color: #2874A6;
        box-shadow: 0 2px 5px rgba(0,0,0,0.2);
    }
    
    /* Sidebar styling */
    .css-1d391kg, .css-1lcbmhc {
        background-color: #F8F9FA;
        padding: 20px;
    }
    
    /* Chat message styling */
    .stChatMessage {
        padding: 12px;
        border-radius: 10px;
        margin-bottom: 12px;
        box-shadow: 0 1px 2px rgba(0,0,0,0.05);
    }
    
    /* User message */
    .stChatMessage[data-testid*="user"] {
        background-color: #E3F2FD;
        border: 1px solid #BBDEFB;
    }
    
    /* Assistant message */
    .stChatMessage[data-testid*="assistant"] {
        background-color: #F8F9FA;
        border: 1px solid #ECEFF1;
    }
    
    /* Header styling */
    h1 {
        color: #2E86C1;
        font-weight: 600;
        font-size: 2.2rem;
        margin-bottom: 0.5rem;
    }
    
    /* Subheader */
    .subheader {
        color: #555;
        font-size: 1.1rem;
        margin-bottom: 2rem;
        font-weight: 400;
    }
    
    /* Chat container */
    .chat-container {
        padding: 20px;
        border-radius: 10px;
        background-color: white;
        margin-bottom: 20px;
    }
    
    /* Spinner */
    .stSpinner > div {
        border-color: #2E86C1 !important;
    }
    
    /* Tabs styling */
    .tab-content {
        padding: 15px 0;
    }
    
    /* Textarea for system prompt */
    .stTextArea textarea {
        border-radius: 8px;
        border: 1px solid #E0E0E0;
        padding: 10px;
        font-size: 14px;
        min-height: 120px;
    }
</style>
""", unsafe_allow_html=True)

# Create a header section
st.markdown('<h1>AI Chatbot</h1>', unsafe_allow_html=True)
st.markdown('<p class="subheader">Your professional AI chatbot ready to help with any questions you might have.</p>', unsafe_allow_html=True)

# Add a horizontal line
st.markdown('<hr style="height:2px;border:none;color:#f0f0f0;background-color:#f0f0f0;margin-bottom:20px;">', unsafe_allow_html=True)

# Chat container
st.markdown('<div class="chat-container">', unsafe_allow_html=True)

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

if "gemini_history" not in st.session_state:
    st.session_state.gemini_history = []

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

st.markdown('</div>', unsafe_allow_html=True)

# Chat input
user_input = st.chat_input("Ask me anything...")

# When user sends a message
if user_input:
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(user_input)
    
    # Get response from AI
    with st.spinner("Processing..."):
        response, history = get_gemini_response(
            user_input, 
            st.session_state.gemini_history, 
            system_prompt=st.session_state.system_prompt,
            temperature=st.session_state.temperature
        )
        st.session_state.gemini_history = history
    
    # Display assistant response
    with st.chat_message("assistant"):
        st.markdown(response)
    
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})
    
    # Force a rerun to update the UI - better user experience
    st.rerun()

# Sidebar with tabs for About and Settings
with st.sidebar:
    st.title("Chatbot Panel")
    
    # Tabs for About and Settings - fixed accessibility warning by adding proper label
    tab_selection = st.radio(
        "Select tab", 
        ["About", "Settings"],
        index=0 if st.session_state.sidebar_tab == "About" else 1,
        horizontal=True,
        label_visibility="collapsed"
    )
    st.session_state.sidebar_tab = tab_selection
    
    # Horizontal line
    st.markdown("<hr>", unsafe_allow_html=True)
    
    if tab_selection == "About":
        # About tab content
        st.markdown("""
        ### Professional AI Chatbot
        This AI chatbot is designed to help you with a wide range of questions and tasks.
        
        ### How to use:
        1. Type your message in the input field
        2. Press Enter to send
        3. The chatbot will respond to your query
        
        ### Features:
        - Natural language understanding
        - Contextual responses
        - Conversation memory
        """)
        
    else:
        # Settings tab content
        st.markdown("### Chatbot Settings")
        st.markdown("Customize how the chatbot responds to your queries.")
        
        # System prompt input
        st.markdown("##### System Prompt")
        st.markdown("This defines the chatbot's personality and behavior")
        system_prompt = st.text_area(
            "System Prompt", 
            value=st.session_state.system_prompt,
            height=150,
            key="system_prompt_input",
            help="This message guides how the AI responds"
        )
        
        # Model temperature
        st.markdown("##### Temperature")
        st.markdown("Higher values make responses more creative, lower values make them more deterministic")
        temperature = st.slider(
            "Temperature", 
            min_value=0.0, 
            max_value=1.0, 
            value=st.session_state.temperature,
            step=0.1,
            key="temperature_input",
            help="Controls randomness: lower is more focused, higher is more creative"
        )
        
        # Save settings button
        if st.button("Save Settings"):
            st.session_state.system_prompt = system_prompt
            st.session_state.temperature = temperature
            st.success("Settings saved!")
    
    # Add some space
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Clear chat button (shown in both tabs)
    if st.button("Clear Conversation", key="clear_chat"):
        st.session_state.messages = []
        st.session_state.gemini_history = []
        st.rerun()
        
    # Add version information at the bottom
    st.markdown("<br><hr><p style='font-size: 0.8rem; color: #888;'>Version 1.0.0</p>", unsafe_allow_html=True) 