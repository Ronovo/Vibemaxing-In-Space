# Space Station Explorer

A simple menu-based space station exploring game built with Python and Tkinter.

## Features

- Main menu with New Game, Load Game, and Quit options
- Character creation with name input and job selection
- Exploration of your personal quarters with interactive objects
- Inventory system with items to collect, view, and store
- Character sheet displaying your stats and inventory
- Complete station hallway navigation system with a full circuit layout
- Continuously running stock market simulation that persists even when not viewing
- Save/load game functionality using JSON files
- Stock market mini-game where you can trade shares and earn credits

## Requirements

- Python 3.x
- Tkinter (usually comes with Python installation)
- Matplotlib (for stock market graphs)

## Installation

```
pip install -r requirements.txt
```

## How to Run

1. Make sure Python is installed on your system
2. Navigate to the game directory
3. Run the game with:

```
python game/main.py
```

## Gameplay

1. Start a new game from the main menu
2. Create your character by entering a name and selecting a job
3. Explore your quarters by interacting with objects:
   - Bed
   - Storage Locker (contains collectible items)
   - Computer (gives access to the Stock Market)
   - Door to the hallway
4. Manage your inventory:
   - Take items from the storage locker
   - View your inventory from the character sheet
   - Return items to the storage locker
5. Explore the space station:
   - Navigate through hallways in cardinal directions (North, South, East, West)
   - The station has a complete circuit layout you can walk around
   - Access your quarters from the hallway junction at coordinates (0,0)
6. Use the computer to access the Stock Market:
   - The stock market runs continuously in the background
   - Stock prices update automatically every 60 seconds
   - Buy and sell shares in various companies
   - Monitor price changes in real-time
   - View price history graphs
   - Earn credits through successful trading
   - Your portfolio and profits are saved when you exit
7. Save your game progress at any time using the "Save and Exit" button
8. Load your saved game from the main menu

## Station Layout

The space station has a complete circuit layout that you can navigate around:
- The crew quarters are accessible from coordinates (0,0) - the starting junction
- The North hallway runs from (0,0) to (5,0)
- The East hallway runs from (0,0) to (0,5)
- From the North end (5,0), you can go East to follow the upper corridor
- From the East end (0,5), you can go North to follow the right corridor
- The far corner at (5,5) connects the upper and right corridors
- You can navigate around the entire circuit in either direction
- Your current coordinates are displayed as (North, East)

## Stock Market Features

The stock market system has the following features:
- Runs continuously in the background during gameplay
- Updates every 60 seconds, even when you're not viewing it
- Saved with your game progress
- When loaded, continues from where it left off
- Stock prices fluctuate based on realistic market conditions
- Portfolio of owned shares persists through saves and loads
- Gains and losses are automatically reflected in your credits

## Note

This is a text/menu-based game with a simple interface. Future updates may include:
- More areas to explore
- Additional items and interactions
- Character stats and progression
- Mission system 