#!/usr/bin/env python3
"""
Run script for Space Station Explorer game
"""

import sys
import os

# Check Python version
if sys.version_info < (3, 6):
    print("This game requires Python 3.6 or higher")
    sys.exit(1)

# Try to import required modules
try:
    import tkinter as tk
    import matplotlib
except ImportError as e:
    print(f"Error: Missing required module: {e}")
    print("Please install required modules with: pip install -r requirements.txt")
    sys.exit(1)

# Run the game
if __name__ == "__main__":
    # Import and run the game
    try:
        from game.main import SpaceStationGame
        
        root = tk.Tk()
        app = SpaceStationGame(root)
        root.mainloop()
    except Exception as e:
        print(f"Error starting game: {e}")
        sys.exit(1) 