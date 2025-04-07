import json
import os
import tkinter as tk
from tkinter import messagebox

class Game:
    """Static utility class with game-wide functions"""
    
    @staticmethod
    def save_game(player_data):
        """Save the game to a JSON file"""
        # Create saves directory if it doesn't exist
        if not os.path.exists("game/saves"):
            os.makedirs("game/saves")
        
        # Save game to JSON file
        filename = f"game/saves/{player_data['name']}.json"
        try:
            with open(filename, "w") as f:
                json.dump(player_data, f, indent=4)
            return True
        except Exception as e:
            print(f"Error saving game: {e}")
            return False
    
    @staticmethod
    def load_game(filename):
        """Load a game from a JSON file"""
        try:
            with open(f"game/saves/{filename}", "r") as f:
                player_data = json.load(f)
            return player_data
        except Exception as e:
            print(f"Error loading game: {e}")
            return None 