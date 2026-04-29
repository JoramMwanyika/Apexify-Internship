from flask import Flask, jsonify, request, send_from_directory
from main import RockPaperScissorsAI

app = Flask(__name__)

# Instantiate our AI game logic
game_ai = RockPaperScissorsAI()

@app.route('/')
def serve_index():
    return send_from_directory('static', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('static', path)

@app.route('/api/play', methods=['POST'])
def play_round():
    data = request.json
    user_move = data.get('move')
    
    if user_move not in ['rock', 'paper', 'scissors']:
        return jsonify({"error": "Invalid move"}), 400
        
    comp_move = game_ai.get_computer_move()
    result = game_ai.determine_winner(user_move, comp_move)
    
    # Store user history for AI to learn
    game_ai.user_history.append(user_move)
    
    return jsonify({
        "user_move": user_move,
        "computer_move": comp_move,
        "result": result,
        "scores": game_ai.scores
    })

@app.route('/api/reset', methods=['POST'])
def reset_game():
    game_ai.user_history = []
    game_ai.scores = {"user": 0, "computer": 0, "draws": 0}
    return jsonify({"message": "Game reset successful", "scores": game_ai.scores})

if __name__ == '__main__':
    # Run the Flask app on port 5000
    app.run(debug=True, port=5000)
