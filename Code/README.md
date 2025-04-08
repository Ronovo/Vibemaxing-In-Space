# Space Station Explorer v7.1.0

A text-based exploration game set on a space station, built with Python and Tkinter.

## Features

### Core Gameplay
- Explore a space station through a menu-driven interface
- Navigate between different rooms and hallways
- Interact with objects and NPCs in each location
- Collect and manage inventory items
- Save and load game progress
- Random events while exploring hallways (20% chance)

### Character System
- Create a character with a custom name
- Choose from 7 different jobs:
  - Staff Assistant (1000 credits)
  - Engineer (2500 credits, Engineering access)
  - Security Guard (5000 credits, Security access)
  - Doctor (7500 credits, MedBay access)
  - Bartender (3500 credits, Bar access, drink-making abilities)
  - Botanist (3000 credits, Botany access, plant cultivation)
  - Head of Personnel (9000 credits, HoP Station, Bar access, Botany access)
  - Captain (10000 credits, full station access)
- Job-specific access to specialized station areas
- Limb health tracking (head, chest, arms, legs)
- Character journal with timestamped notes of significant events

### Special Rooms
- **Quarters**: Personal living space with storage, bed, and computer
- **MedBay**: Medical facility with health checks and treatment options
- **Bridge**: Command center for station operations
- **Security**: Monitoring and security systems
- **Engineering Bay**: Maintenance center with tools and equipment
- **Bar**: Social area with drinks, books, and relaxation options
- **Botany Lab**: Plant cultivation and research facility

### Botany System
- Collect seeds from the seed machine
- Plant and grow different types of plants in dedicated planters
- Monitor plant growth and development
- Job-specific access to botany station controls

### Stock Market
- Real-time stock market simulation
- Buy and sell shares in various companies
- Track market cycles and trade history
- Make profits through smart trading
- Transaction logging with profit/loss tracking
- Filter stocks by affordability and ownership
- Sort stocks by price (low to high or high to low)
- Colorful trade history display
- Scrollable interface for all market functionality

### Bar System
- Interactive bar counter for ordering and mixing drinks
- Wide variety of ingredients and recipes
- Special bartender job with unique drink-making abilities
- Drink effects can restore health or provide other benefits
- Recipe discovery through exploration and experimentation

### Book Reading System
- Collection of readable books throughout the station
- Detailed stories and station lore accessible through reading
- Multiple pages with pagination controls
- Knowledge about station history, systems, and characters

### Advanced Features
- Role-based access control to specialized station systems
- Door locking/unlocking for authorized personnel
- Cycle-based trade logging in stock market
- Circuit-based station navigation system
- Random event system (good, bad, and neutral outcomes)
- Limb damage and medical treatment system
- Scrollable storage interface with expanded inventory options
- Character notes system tracking important events
- Enhanced scrollable interfaces for better user experience

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
python run_game.py
```

## Standalone Executable

A standalone executable version is available for Windows:

1. Download the latest release from the releases page
2. Extract the zip file
3. Run the space_station_explorer.exe file

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
   - Find random items while exploring hallways
5. Explore the space station:
   - Navigate through hallways in cardinal directions (North, South, East, West)
   - The station has a complete circuit layout you can walk around
   - Access your quarters from the hallway junction at coordinates (0,0)
   - Random events may occur while moving through hallways
6. Visit the Bar:
   - Order drinks from the bartender
   - Read books and learn about station lore
   - If you're a bartender, mix drinks for yourself with various ingredients
   - Discover new drink recipes through experimentation
7. Visit the Botany Lab:
   - View plants being grown in the lab
   - If you have access, collect seeds from the seed machine
   - Plant seeds in dedicated planters
   - Monitor plant growth and development
8. Use the computer to access the Stock Market:
   - The stock market runs continuously in the background
   - Stock prices update automatically every 60 seconds
   - Buy and sell shares in various companies
   - Monitor price changes in real-time
   - View price history graphs
   - Filter stocks by affordability and ownership status
   - Sort stocks by price (low to high or high to low)
   - View detailed trade history with color-coded entries
   - Earn credits through successful trading
   - Your portfolio and profits are saved when you exit
9. Monitor and manage your character's health:
   - Check your limb health status on the character sheet
   - Receive medical treatment in the MedBay
   - Pay for healing services (50 credits)
   - Special healing options for authorized medical personnel
   - Consume certain drinks to recover health
10. Track your character's journey:
   - View notes about important events
   - See records of injuries, financial transactions, and discoveries
   - Timestamped entries in reverse chronological order
11. Save your game progress at any time using the "Save and Exit" button
12. Load your saved game from the main menu

## Station Layout

The space station has a complete circuit layout that you can navigate around:
- The crew quarters are accessible from coordinates (0,0) - the starting junction
- The North hallway runs from (0,0) to (5,0)
- The East hallway runs from (0,0) to (0,5)
- From the North end (5,0), you can go East to follow the upper corridor
- From the East end (0,5), you can go North to follow the right corridor
- The Engineering Bay is accessible from coordinates (5,3)
- The Bar is accessible from coordinates (0,3)
- The Botany Lab is accessible from coordinates (3,0)
- The far corner at (5,5) connects the upper and right corridors
- You can navigate around the entire circuit in either direction
- Your current coordinates are displayed as (North, East)

## Special Room Access

Each job comes with different room access permissions:
- **Staff Assistant**: No special access
- **Engineer**: Engineering Bay access
- **Security Guard**: Security access
- **Doctor**: MedBay access
- **Bartender**: Bar access (can mix drinks)
- **Botanist**: Botany Lab access (can cultivate plants)
- **Head of Personnel**: HoP Station, Bar, and Botany Lab access
- **Captain**: Full access to all rooms

Locked doors can only be opened by personnel with proper authorization.

## Medical System

The game features a comprehensive health system:
- Each character has 6 limbs with individual health percentages
- Injuries can occur during random events in hallways
- Medical scans show detailed health reports with recommendations
- Doctors can provide advanced treatment in the MedBay
- Anyone can pay 50 credits for medical services
- Certain drinks can provide health benefits when consumed
- Doors can be locked/unlocked by authorized personnel

## Stock Market Features

The stock market system has the following features:
- Runs continuously in the background during gameplay
- Updates every 60 seconds, even when you're not viewing it
- Saved with your game progress
- When loaded, continues from where it left off
- Stock prices fluctuate based on realistic market conditions
- Portfolio of owned shares persists through saves and loads
- Gains and losses are automatically reflected in your credits
- Transactions are logged in your character notes
- Filter options to view only Affordable/Expensive stocks
- Filter options to view only Owned/Not Owned stocks
- Sorting options by price (Low to High or High to Low)
- Colorful trade history display with chronological entries
- Scrollable interface for ease of use

## Bar System

The bar area offers several features:
- Order drinks from a menu if a bartender NPC is present
- As a bartender, mix your own drinks using various ingredients
- Discover new recipes through experimentation
- Drink effects can include health restoration or other benefits
- Read books to learn about station history and lore
- Social space for relaxation between explorations

## Book Reading System

The game includes a book reading system:
- Books can be found in various locations around the station
- Each book contains multiple pages of text
- Navigate through pages with Previous and Next buttons
- Books contain information about station history, systems, and characters
- Some books may provide hints about game mechanics or secrets

## Botany System

The Botany Lab has the following features:
- Seed Machine with 5 different types of seeds
- 4 planters for growing different plants
- Plant growth stages from seedling to maturity
- Botanist role with special access to the lab
- Captain and Head of Personnel also have lab access
- All personnel can view plants in the lab

## Future Updates

Planned features for future versions:
- More areas to explore
- Additional items and interactions
- Character stats and progression
- Mission system
- Crafting system
- NPC interactions and dialogue
- Equipment and gear system 