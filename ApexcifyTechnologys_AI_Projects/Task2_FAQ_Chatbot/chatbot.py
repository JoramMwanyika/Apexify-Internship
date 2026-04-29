import json
import numpy as np
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import string

# Safely download required NLTK resources by catching all exceptions
for resource in ['punkt', 'punkt_tab', 'stopwords']:
    try:
        if 'punkt' in resource:
            nltk.data.find(f'tokenizers/{resource}')
        else:
            nltk.data.find(f'corpora/{resource}')
    except Exception:
        nltk.download(resource, quiet=True)

class IntentDetector:
    """
    A simple Intent Detection Layer using TF-IDF and Cosine Similarity
    to classify the user's intent before searching the FAQ database.
    """
    def __init__(self):
        # Define basic intents and some training phrases
        self.intents = {
            "greeting": ["hello", "hi", "hey", "good morning", "good afternoon", "greetings"],
            "farewell": ["bye", "goodbye", "see you later", "exit", "quit", "cya"],
            "gratitude": ["thank you", "thanks", "appreciate it"],
            "faq_query": ["how do I", "why is", "what is", "can you help", "issue", "problem", "laptop", "password", "screen", "fix"]
        }
        self.vectorizer = TfidfVectorizer()
        self.intent_labels = []
        self.training_phrases = []
        
        for intent, phrases in self.intents.items():
            for phrase in phrases:
                self.training_phrases.append(phrase)
                self.intent_labels.append(intent)
                
        # Train the intent vectorizer
        self.tfidf_matrix = self.vectorizer.fit_transform(self.training_phrases)

    def detect_intent(self, user_query):
        query_vec = self.vectorizer.transform([user_query.lower()])
        similarities = cosine_similarity(query_vec, self.tfidf_matrix)
        best_match_idx = np.argmax(similarities)
        highest_score = similarities[0, best_match_idx]
        
        # If the highest score is above a small threshold, we consider it a match
        if highest_score > 0.15:
            return self.intent_labels[best_match_idx]
        return "unknown" # Default if no strong match

class FAQChatbot:
    def __init__(self, data_path='faq_data.json'):
        self.data_path = data_path
        self.faq_data = []
        self.questions = []
        self.answers = []
        
        # Initialize NLP tools
        self.vectorizer = TfidfVectorizer()
        self.tfidf_matrix = None
        self.stop_words = set(stopwords.words('english'))
        
        # Initialize Intention Detection Layer
        self.intent_detector = IntentDetector()
        
        self.load_data()
        self.train()

    def load_data(self):
        try:
            with open(self.data_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
                # Handle both the old list format and the new nested 'faqs' dictionary format
                if isinstance(data, dict) and 'faqs' in data:
                    self.faq_data = data['faqs']
                elif isinstance(data, list):
                    self.faq_data = data
                else:
                    self.faq_data = []
            
            for item in self.faq_data:
                self.questions.append(item['question'])
                self.answers.append(item['answer'])
        except FileNotFoundError:
            print(f"Error: Could not find {self.data_path}. Please ensure the file exists.")
            exit(1)

    def preprocess_text(self, text):
        """
        Cleans and tokenizes text.
        """
        text = text.lower()
        tokens = word_tokenize(text)
        
        clean_tokens = [
            word for word in tokens 
            if word not in string.punctuation and word not in self.stop_words
        ]
        
        return " ".join(clean_tokens)

    def train(self):
        """
        Preprocesses all FAQ questions and fits the TF-IDF vectorizer.
        """
        processed_questions = [self.preprocess_text(q) for q in self.questions]
        self.tfidf_matrix = self.vectorizer.fit_transform(processed_questions)

    def get_response(self, user_query):
        """
        Combines Intent Detection with FAQ Cosine Similarity Matching.
        """
        # Step 1: Detect Intent
        intent = self.intent_detector.detect_intent(user_query)
        
        # Step 2: Preprocess the query for FAQ matching
        processed_query = self.preprocess_text(user_query)
        
        if not processed_query.strip() and intent == "unknown":
            return intent, "I'm sorry, I didn't catch that. Could you please rephrase?"

        # Step 3: Match against FAQs
        query_vector = self.vectorizer.transform([processed_query])
        similarities = cosine_similarity(query_vector, self.tfidf_matrix)
        
        best_match_idx = np.argmax(similarities)
        highest_score = similarities[0, best_match_idx]
        
        # Define a threshold for finding a matching FAQ
        threshold = 0.2
        if highest_score < threshold:
            # Fallback to pure intent-based responses if FAQ fails
            if intent == "greeting":
                return intent, "Hello! How can I help you today?"
            elif intent == "farewell":
                return intent, "Goodbye! Have a great day!"
            elif intent == "gratitude":
                return intent, "You're very welcome!"
                
            return intent, "I'm sorry, I don't have an answer to that question in my database. Could you try asking something else?"
            
        return intent, self.answers[best_match_idx]

def run_cli_chatbot():
    chatbot = FAQChatbot()
    print("🤖 AI FAQ Chatbot Initialized (with Intention Detection)!")
    print("Ask me anything. Type 'quit' or 'exit' to stop.\n")
    
    while True:
        user_input = input("You: ").strip()
        
        if user_input.lower() in ['quit', 'exit']:
            print("Chatbot: [Intent: FAREWELL] Goodbye! Have a great day!")
            break
            
        intent, response = chatbot.get_response(user_input)
        print(f"Chatbot [Intent: {intent.upper()}]: {response}\n")

if __name__ == "__main__":
    run_cli_chatbot()
