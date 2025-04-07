# Space Station Explorer v5.0.0

A text-based exploration game set on a space station, built with Python and Tkinter.

## Features

### Core Gameplay
- Explore a space station through a menu-driven interface
- Navigate between different rooms and hallways
- Interact with objects and NPCs in each location
- Collect and manage inventory items
- Save and load game progress

### Character System
- Create a character with a custom name
- Choose from 5 different jobs:
  - Staff Assistant (1000 credits)
  - Engineer (2500 credits)
  - Security Guard (5000 credits, Security access)
  - Doctor (7500 credits, MedBay access)
  - Captain (10000 credits, full station access)
- Job-specific access to specialized station areas

### Special Rooms
- **Quarters**: Personal living space with storage, bed, and computer
- **MedBay**: Medical facility with health checks and specialized equipment
- **Bridge**: Command center for station operations
- **Security**: Monitoring and security systems

### Stock Market
- Real-time stock market simulation
- Buy and sell shares in various companies
- Track market cycles and trade history
- Make profits through smart trading

### Advanced Features
- Role-based access control to specialized station systems
- Door locking/unlocking for authorized personnel
- Cycle-based trade logging in stock market
- Circuit-based station navigation system

## Controls
- Use buttons and menus to navigate and interact
- Character-specific controls appear based on your job
- Save your game by using your bed or the Save button

## Getting Started
1. Run `python run_game.py`
2. Create a new character or load an existing one
3. Explore the station and discover its secrets

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