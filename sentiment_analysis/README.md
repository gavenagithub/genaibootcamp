# Data Science Notebooks

This repository contains Jupyter notebooks for machine learning and natural language processing tasks:

- `sentiment_analysis_model.ipynb`: A sentiment analysis model that classifies text as positive, negative, or neutral
- `Digit Classification.ipynb`: A neural network for handwritten digit classification
- `sentiment_app.py`: A Streamlit web application for the sentiment analysis model

## Setting Up Your Environment

### 1. Install Python

Ensure you have Python 3.8+ installed on your system. You can download it from [python.org](https://www.python.org/downloads/).

### 2. Create a Virtual Environment

A virtual environment is recommended to manage dependencies without affecting other Python projects.

#### On macOS/Linux:

```bash
# Navigate to the project directory
cd /path/to/genaibootcamp/sentiment_analysis

# Create a virtual environment
python3.10 -m venv new_env

# Activate the virtual environment
source new_env/bin/activate
```

#### On Windows:

```bash
# Navigate to the project directory
cd \path\to\genaibootcamp

# Create a virtual environment
python3.10 -m venv new_env

# Activate the virtual environment
new_env\Scripts\activate
```

### 3. Install Dependencies

Install all required packages using pip:

```bash
# Make sure your virtual environment is activated
pip install -r requirements.txt
```

### 4. Launch Jupyter Notebook

Start the Jupyter Notebook server:

```bash
jupyter notebook
```

This will open a browser window showing your project directory. Click on any notebook (.ipynb file) to open it.

## Running the Notebooks

### Sentiment Analysis Model

The `sentiment_analysis_model.ipynb` notebook demonstrates:
- Generating synthetic training data for sentiment analysis
- Processing text data with TF-IDF vectorization
- Training Multinomial Naive Bayes and Logistic Regression models
- Evaluating model performance
- Interactive testing with custom text input

### Digit Classification

The `Digit Classification.ipynb` notebook covers:
- Loading and preprocessing image data for handwritten digit recognition
- Building a neural network model using TensorFlow/Keras
- Training and evaluating the model
- Visualizing results

## Streamlit Web Application

The repository includes a Streamlit application for sentiment analysis that provides a user-friendly web interface:

### Running the Streamlit App

To run the sentiment analysis web application:

```bash
# Make sure your virtual environment is activated
streamlit run sentiment_app.py
```

The application allows you to:
- Enter custom text for sentiment analysis
- See sentiment predictions (positive, negative, or neutral) with confidence scores
- View probability distributions for each sentiment category
- Try example texts with predefined samples

### Requirements

The Streamlit app requires:
- The trained sentiment analysis model (`sentiment_model.joblib`)
- The TF-IDF vectorizer (`tfidf_vectorizer.joblib`)
- Streamlit library (installed via requirements.txt)

## Machine Learning Models

The repository includes pre-trained models:

- `sentiment_model.joblib`: A trained sentiment analysis model
- `tfidf_vectorizer.joblib`: The TF-IDF vectorizer for text preprocessing

These models are used by both the Jupyter notebook and the Streamlit application.

## Troubleshooting

### Common Issues

1. **Package not found errors**:
   - Make sure you've activated your virtual environment
   - Try reinstalling the specific package: `pip install package_name`

2. **Kernel dying in Jupyter**:
   - This often happens due to memory issues
   - Try closing other applications or restarting your notebook

3. **CUDA errors with TensorFlow**:
   - For Mac with Apple Silicon, make sure you're using tensorflow-macos and tensorflow-metal
   - For other systems, ensure you have compatible CUDA drivers

4. **Streamlit app fails to load models**:
   - Check that you're running the app from the same directory where the .joblib files are located
   - Verify that the model files were created correctly by running the notebook first

### Getting Help

If you encounter issues:
1. Check the error message for specific package version conflicts
2. Search for the error online
3. Consider opening an issue in the repository

## Additional Resources

- [Scikit-learn Documentation](https://scikit-learn.org/stable/)
- [TensorFlow Documentation](https://www.tensorflow.org/api_docs)
- [Jupyter Notebook Documentation](https://jupyter-notebook.readthedocs.io/en/stable/)
- [Streamlit Documentation](https://docs.streamlit.io/)