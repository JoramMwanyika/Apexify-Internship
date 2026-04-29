# Task 1: Rock-Paper-Scissors with AI Opponent (Web GUI)

A modern, premium web application where you play Rock-Paper-Scissors against the computer. 
The computer uses a probability-based AI mechanism: it tracks your past moves, predicts your next move based on your most frequent choice, and strategically plays the counter-move to beat you!

## Features
- **Premium Graphical UI**: Smooth animations, glassmorphism design, and AI-generated 3D hand graphics.
- **REST API Backend**: Flask handles the game logic and state.
- **Adaptive AI**: The AI learns from your history to counter your playstyle.

## Setup Instructions

1. Ensure you have Python installed (Python 3.x is recommended).
2. Open a terminal or command prompt.
3. Navigate to this project folder (`Task1_RockPaperScissors_AI`).
4. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
5. Run the web server:
   ```bash
   python app.py
   ```
6. Open your web browser and go to: **http://127.0.0.1:5000**

## How the AI Works

1. The AI stores every move the user makes.
2. When determining its next move, it counts the frequencies of the user's past moves.
3. It identifies the user's most frequently played move.
4. It selects the move that defeats the predicted user move.
5. In the early rounds, it falls back to a random choice.
