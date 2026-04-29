import random
from collections import Counter

# Game Logic Mapping
# Key beats Value
WINNING_MOVES = {
    "rock": "scissors",
    "paper": "rock",
    "scissors": "paper"
}

# The reverse mapping: what loses to Key
LOSING_MOVES = {
    "rock": "paper",
    "paper": "scissors",
    "scissors": "rock"
}

VALID_MOVES = ["rock", "paper", "scissors"]

class RockPaperScissorsAI:
    def __init__(self):
        self.user_history = []
        self.scores = {"user": 0, "computer": 0, "draws": 0}
        
    def predict_user_move(self):
        """
        Simple probability-based AI:
        Finds the user's most frequently played move.
        If history is too short or tied, return a random move.
        """
        if len(self.user_history) < 2:
            return random.choice(VALID_MOVES)
            
        # Count frequencies of past user moves
        move_counts = Counter(self.user_history)
        
        # Get the most common move
        most_common_move = move_counts.most_common(1)[0][0]
        
        return most_common_move

    def get_computer_move(self):
        """
        The computer decides its move based on predicting the user's move,
        then picking the move that defeats it.
        """
        predicted_user_move = self.predict_user_move()
        # Pick the move that beats the predicted user move
        counter_move = LOSING_MOVES[predicted_user_move]
        return counter_move

    def determine_winner(self, user_move, comp_move):
        if user_move == comp_move:
            self.scores["draws"] += 1
            return "Draw!"
        elif WINNING_MOVES[user_move] == comp_move:
            self.scores["user"] += 1
            return "You win!"
        else:
            self.scores["computer"] += 1
            return "Computer wins!"

    def display_scores(self):
        print("\n--- Current Score ---")
        print(f"User: {self.scores['user']} | Computer: {self.scores['computer']} | Draws: {self.scores['draws']}")
        print("---------------------\n")

    def play(self):
        print("🤖 Welcome to Rock-Paper-Scissors with AI! 🤖")
        print("Type 'quit' or 'exit' to stop playing.\n")
        
        while True:
            user_input = input("Enter your move (rock/paper/scissors): ").lower().strip()
            
            if user_input in ['quit', 'exit']:
                print("\nThanks for playing!")
                self.display_scores()
                break
                
            if user_input not in VALID_MOVES:
                print("Invalid move. Please choose 'rock', 'paper', or 'scissors'.")
                continue
                
            comp_move = self.get_computer_move()
            print(f"Computer chose: {comp_move.capitalize()}")
            
            result = self.determine_winner(user_input, comp_move)
            print(f"Result: {result}")
            
            # Store user history for the AI to learn
            self.user_history.append(user_input)
            
            self.display_scores()

if __name__ == "__main__":
    game = RockPaperScissorsAI()
    game.play()
