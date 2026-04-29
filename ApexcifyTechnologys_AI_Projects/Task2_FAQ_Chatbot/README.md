# Task 2: FAQ Chatbot (NLP-Based)

An intelligent Command Line Interface (CLI) chatbot built with Python. This chatbot uses Natural Language Processing (NLP) techniques to understand user queries and match them to the most relevant frequently asked questions (FAQs).

## How it works
1. **Preprocessing:** Uses `nltk` to convert text to lowercase, remove punctuation, tokenize words, and remove stopwords (e.g., "the", "is").
2. **Vectorization:** Uses `scikit-learn`'s `TfidfVectorizer` to convert text strings into numerical vectors (TF-IDF).
3. **Similarity Matching:** Computes the **Cosine Similarity** between the vectorized user query and the vectorized FAQ dataset to find the best match.
4. **Response:** Returns the answer of the best-matched question.

## Setup Instructions

1. Ensure Python 3.x is installed.
2. Navigate to this directory (`Task2_FAQ_Chatbot`).
3. Install the required Python libraries:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the chatbot:
   ```bash
   python chatbot.py
   ```
   *(Note: On its first run, it may take a few seconds to verify/download NLTK data like tokenizers and stopwords.)*

## Customization
You can easily add more FAQs by editing the `faq_data.json` file. Ensure it remains valid JSON format.
