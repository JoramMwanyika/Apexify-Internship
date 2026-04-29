from flask import Flask, request, jsonify, send_from_directory
from chatbot import FAQChatbot
import os

app = Flask(__name__)

# Initialize the chatbot (this will trigger NLP processing and training on startup)
chatbot_engine = FAQChatbot()

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('static', path)

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message', '')
    
    if not user_message:
        return jsonify({"error": "Empty message"}), 400
        
    # Get the detected intent and the appropriate response
    intent, response = chatbot_engine.get_response(user_message)
    
    return jsonify({
        "intent": intent.upper(),
        "response": response
    })

if __name__ == '__main__':
    print("Starting IT Assistant Chatbot Server...")
    app.run(debug=True, port=5000)
