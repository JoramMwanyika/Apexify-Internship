# Task 2: FAQ Chatbot (IT Assistant Web UI)

An intelligent, modern Web Chatbot built with Python, NLP (NLTK & Scikit-Learn), and Flask.

This chatbot serves as an IT Assistant. It uses Natural Language Processing to detect the intent of your message (e.g., Greeting, Farewell, FAQ Query) and then uses TF-IDF Vectorization and Cosine Similarity to find the best answer to your question from a custom JSON database.

## Features
- **Intention Detection Layer**: Understands greetings, farewells, and gratitude before checking the FAQ database.
- **Modern Messenger UI**: A premium, responsive web interface built with pure CSS and JS, featuring typing indicators and intent badges.
- **NLP Preprocessing**: Lowercasing, punctuation removal, tokenization, and stopword filtering.

## Setup Instructions

1. Ensure Python 3.x is installed.
2. Navigate to this directory (`Task2_FAQ_Chatbot`).
3. Install the required Python libraries:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the Flask Web Server:
   ```bash
   python app.py
   ```
5. Open your web browser and go to: **http://127.0.0.1:5000**

## Customization
You can add more FAQs by editing the `faq_data.json` file. The backend will automatically train on the new data the next time you start the server!
