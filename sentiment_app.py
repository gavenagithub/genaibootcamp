import streamlit as st
import joblib
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Set page configuration
st.set_page_config(page_title="Sentiment Analysis App", layout="wide")

# Load the saved model and vectorizer
@st.cache_resource
def load_model():
    model = joblib.load('sentiment_model.joblib')
    vectorizer = joblib.load('tfidf_vectorizer.joblib')
    return model, vectorizer

# Function to predict sentiment
def predict_sentiment(text, model, vectorizer):
    # Preprocess the input text using the saved vectorizer
    text_tfidf = vectorizer.transform([text])
    
    # Predict sentiment
    sentiment = model.predict(text_tfidf)[0]
    
    # Get probability scores for each class
    proba = model.predict_proba(text_tfidf)[0]
    
    return sentiment, proba

# Create a function to get color for sentiment
def get_sentiment_color(sentiment):
    if sentiment == 'positive':
        return "#28a745"  # Green
    elif sentiment == 'negative':
        return "#dc3545"  # Red
    else:
        return "#6c757d"  # Gray for neutral

# Main function
def main():
    # App title
    st.title("Sentiment Analysis Tool")
    
    # Load model and vectorizer
    with st.spinner("Loading model..."):
        model, vectorizer = load_model()
    
    # App description
    st.write("""
    This application analyzes the sentiment of your text and classifies it as positive, negative, or neutral.
    Enter your text below and click 'Analyze' to get started!
    """)
    
    # Text input
    user_input = st.text_area("Enter text for sentiment analysis:", height=150)
    
    # Create columns for button alignment
    col1, col2, col3 = st.columns([1, 1, 5])
    
    # Submit button
    with col1:
        submit_button = st.button("Analyze")
    
    # Clear button
    with col2:
        clear_button = st.button("Clear")
    
    # Handle clear button
    if clear_button:
        st.session_state.user_input = ""
        st.rerun()
    
    # Examples
    with st.expander("Show example texts"):
        examples = [
            "I absolutely loved the movie, it was fantastic!",
            "The service was terrible and the staff was rude.",
            "The restaurant was okay, nothing special.",
            "I'm not sure how I feel about this product yet."
        ]
        
        for i, example in enumerate(examples):
            if st.button(f"Example {i+1}"):
                st.session_state.user_input = example
                st.rerun()
    
    # Keep track of input in session state
    if 'user_input' not in st.session_state:
        st.session_state.user_input = ""
    
    if user_input:
        st.session_state.user_input = user_input
    
    # When the button is clicked or input is submitted
    if submit_button and st.session_state.user_input:
        with st.spinner("Analyzing sentiment..."):
            # Get sentiment and probabilities
            sentiment, probabilities = predict_sentiment(st.session_state.user_input, model, vectorizer)
            
            # Display results
            st.markdown("### Analysis Result")
            
            # Create columns for layout
            col1, col2 = st.columns([1, 1])
            
            with col1:
                # Display sentiment with appropriate styling
                sentiment_color = get_sentiment_color(sentiment)
                st.markdown(f"<h2 style='color: {sentiment_color};'>{sentiment.upper()}</h2>", unsafe_allow_html=True)
                
                # Display confidence
                confidence = max(probabilities) * 100
                st.write(f"Confidence: {confidence:.2f}%")
            
            with col2:
                # Create bar chart for probabilities
                fig, ax = plt.subplots(figsize=(8, 2))
                
                # Define class names and colors
                class_names = model.classes_
                colors = ['#dc3545', '#6c757d', '#28a745'] if len(class_names) == 3 else ['#dc3545', '#28a745']
                
                # Plot horizontal bars
                bars = ax.barh(class_names, probabilities, color=colors)
                
                # Add percentage labels
                for i, bar in enumerate(bars):
                    width = bar.get_width()
                    ax.text(width + 0.01, bar.get_y() + bar.get_height()/2, f"{width*100:.1f}%", 
                            ha='left', va='center')
                
                # Set labels and title
                ax.set_xlabel('Probability')
                ax.set_title('Sentiment Probability Distribution')
                ax.set_xlim(0, 1)
                
                # Remove top and right spines
                ax.spines['top'].set_visible(False)
                ax.spines['right'].set_visible(False)
                
                # Show the plot
                st.pyplot(fig)
            
            # Show analyzed text
            st.markdown("### Text Analyzed")
            st.write(st.session_state.user_input)
            
    # Show a warning if no text is entered
    elif submit_button:
        st.warning("Please enter some text to analyze.")

# Run the app
if __name__ == "__main__":
    main()