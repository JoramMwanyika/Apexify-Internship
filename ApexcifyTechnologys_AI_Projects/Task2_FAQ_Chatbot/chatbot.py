import json
import numpy as np
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import string

# Download required NLTK resources
# Suppress the download messages by capturing them or just let them print once
try:
    nltk.data.find('tokenizers/punkt')
    nltk.data.find('tokenizers/punkt_tab')
except LookupError:
    nltk.download('punkt', quiet=True)
    nltk.download('punkt_tab', quiet=True)
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords', quiet=True)

class FAQChatbot:
    def __init__(self, data_path='faq_data.json'):
        self.data_path = data_path
        self.faq_data = []
        self.questions = []
        self.answers = []
        self.vectorizer = TfidfVectorizer()
        self.tfidf_matrix = None
        self.stop_words = set(stopwords.words('english'))
        self.load_data()
        self.train()

    def load_data(self):
        try:
            with open(self.data_path, 'r', encoding='utf-8') as f:
                self.faq_data = json.load(f)
            
            for item in self.faq_data:
                self.questions.append(item['question'])
                self.answers.append(item['answer'])
        except FileNotFoundError:
            print(f"Error: Could not find {self.data_path}. Please ensure the file exists.")
            exit(1)

    def preprocess_text(self, text):
        """
        Cleans and tokenizes text.
        Steps:
        1. Lowercase
        2. Tokenize
        3. Remove punctuation and stop words
        """
        # Lowercase
        text = text.lower()
        
        # Tokenize
        tokens = word_tokenize(text)
        
        # Remove punctuation and stop words
        clean_tokens = [
            word for word in tokens 
            if word not in string.punctuation and word not in self.stop_words
        ]
        
        return " ".join(clean_tokens)

    def train(self):
        """
        Preprocesses all questions and fits the TF-IDF vectorizer.
        """
        processed_questions = [self.preprocess_text(q) for q in self.questions]
        # Transform questions to vectors
        self.tfidf_matrix = self.vectorizer.fit_transform(processed_questions)

    def get_response(self, user_query):
        """
        Finds the most similar question using Cosine Similarity.
        """
        processed_query = self.preprocess_text(user_query)
        
        # If the user enters something completely meaningless
        if not processed_query.strip():
            return "I'm sorry, I didn't catch that. Could you please rephrase?"

        # Transform user query into a vector
        query_vector = self.vectorizer.transform([processed_query])
        
        # Calculate cosine similarity between the user query and all FAQ questions
        similarities = cosine_similarity(query_vector, self.tfidf_matrix)
        
        # Find the index of the highest similarity score
        best_match_idx = np.argmax(similarities)
        highest_score = similarities[0, best_match_idx]
        
        # Define a threshold for "I don't know"
        threshold = 0.2
        if highest_score < threshold:
            return "I'm sorry, I don't have an answer to that question in my database. Could you try asking something else?"
            
        return self.answers[best_match_idx]

def run_cli_chatbot():
    chatbot = FAQChatbot()
    print("🤖 AI FAQ Chatbot Initialized!")
    print("Ask me anything about our company. Type 'quit' or 'exit' to stop.\n")
    
    while True:
        user_input = input("You: ").strip()
        
        if user_input.lower() in ['quit', 'exit']:
            print("Chatbot: Goodbye! Have a great day!")
            break
            
        response = chatbot.get_response(user_input)
        print(f"Chatbot: {response}\n")

if __name__ == "__main__":
    run_cli_chatbot()
