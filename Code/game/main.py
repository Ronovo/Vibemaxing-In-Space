import tkinter as tk
import json
import os
import time
import threading
import datetime
import random
from tkinter import messagebox
from tkinter import simpledialog

# Add the stock market imports
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

# Import the StockMarket class
from game.stock_market import StockMarket
from game.stock_market import Company

# Define the book contents
BOOK_CONTENTS = {
    "Welcome Guide": """WELCOME TO SPACE STATION EXPLORER

Welcome to your new home among the stars! This guide will help you get acquainted with life aboard our station.

IMPORTANT TIPS:
- Always follow safety protocols
- Report any unusual activity to Security
- Keep your personal quarters clean and organized
- Get to know your fellow crew members
- Visit the Bar for social interactions
- Check the computer terminal for stock market opportunities

We hope you enjoy your stay and contribute to our thriving community!
""",
    "Station Map": """SPACE STATION EXPLORER - STATION MAP

NORTH SECTION:
- Bridge (Command Center)
- North Hallway

EAST SECTION:
- Medical Bay
- East Hallway
- Bar

NORTHEAST SECTION:
- Security
- Engineering Bay

CENTRAL:
- Personal Quarters
- Hallway Junction

Remember to use navigation panels to move between sections.
""",
    "Maintenance Manual": """SPACE STATION MAINTENANCE MANUAL

BASIC TROUBLESHOOTING:
1. Power cycling is the first solution to try for most electronic issues
2. Check circuit breakers before reporting electrical failures
3. Small air leaks can be temporarily patched with emergency sealant
4. All maintenance tasks must be logged in the station computer

EMERGENCY PROCEDURES:
- Depressurization: Secure oxygen mask, move to nearest airlock
- Fire: Use extinguisher, then evacuate section
- Power failure: Emergency lighting will activate automatically

Contact Engineering for all major repair needs.
""",
}

class SpaceStationGame:
    def __init__(self, root, base_path):
        self.root = root
        self.root.title("Space Station Explorer")
        self.root.geometry("800x600")
        self.root.configure(bg="black")
        
        # Store base path for file operations
        self.base_path = base_path
        
        # Stock market background tracking
        self.companies = [
            Company("TechCorp", random.uniform(10, 1000)),
            Company("GlobalBank", random.uniform(10, 1000)),
            Company("HealthCare Plus", random.uniform(10, 1000)),
            Company("EnergyCo", random.uniform(10, 1000)),
            Company("FoodChain", random.uniform(10, 1000)),
            Company("AutoMakers", random.uniform(10, 1000)),
            Company("RetailGiant", random.uniform(10, 1000)),
            Company("PharmaTech", random.uniform(10, 1000)),
            Company("RealEstate Co", random.uniform(10, 1000)),
            Company("MediaGroup", random.uniform(10, 1000)),
            Company("Aerospace Inc", random.uniform(10, 1000)),
            Company("TechStart", random.uniform(10, 1000)),
            Company("GreenEnergy", random.uniform(10, 1000)),
            Company("DigitalBank", random.uniform(10, 1000)),
            Company("SmartHome", random.uniform(10, 1000))
        ]
        self.stock_cycle_number = 0
        self.stock_day_number = 1
        self.market_thread = None
        self.market_running = False
        self.last_update_time = datetime.datetime.now()
        
        self.player_data = {
            "name": "",
            "job": "",
            "inventory": [],
            "credits": 1000,  # Add credits to player data
            "location": {"x": 0, "y": 0},  # Add location data for hallway navigation
            "stock_holdings": {},  # Add stock holdings data
            "stock_market": {
                "cycle_number": 0,
                "day_number": 1,
                "companies": [],
                "last_update_time": datetime.datetime.now().isoformat(),
                "trade_log": []  # Add trade log to persist between sessions
            },
            "limbs": {
                "left_arm": 100,
                "right_arm": 100,
                "left_leg": 100,
                "right_leg": 100,
                "chest": 100,
                "head": 100
            },
            "notes": []  # Add notes array to track important events
        }
        
        # Ship map configuration - Updated to include Engineering Bay
        self.ship_map = {
            # Hallway Junction and Main Hallways
            "0,0": {"name": "Hallway Junction", "desc": "A junction in the hallway. Your quarters are nearby."},
            "1,0": {"name": "North Hallway", "desc": "A long hallway stretching north."},
            "2,0": {"name": "North Hallway", "desc": "A long hallway stretching north."},
            "3,0": {"name": "North Hallway", "desc": "A long hallway stretching north."},
            "4,0": {"name": "North Hallway", "desc": "A long hallway stretching north."},
            "5,0": {"name": "North End", "desc": "The northern end of the hallway. The bridge is nearby."},
            "0,1": {"name": "East Hallway", "desc": "A long hallway stretching east."},
            "0,2": {"name": "East Hallway", "desc": "A long hallway stretching east."},
            "0,3": {"name": "Bar Entrance", "desc": "This hallway leads to the station Bar. Soft music can be heard from inside."},
            "0,4": {"name": "East Hallway", "desc": "A long hallway stretching east."},
            "0,5": {"name": "East End", "desc": "The eastern end of the hallway. The medbay is nearby."},
            
            # Northeast Corridors
            "5,1": {"name": "Northeast Hallway", "desc": "A hallway connecting the north and east corridors."},
            "5,2": {"name": "Northeast Hallway", "desc": "A hallway connecting the north and east corridors."},
            "5,3": {"name": "Engineering Bay Entrance", "desc": "This hallway leads to the Engineering Bay."},
            "5,4": {"name": "Northeast Hallway", "desc": "A hallway connecting the north and east corridors."},
            "5,5": {"name": "Northeast Corner", "desc": "The far corner of the station. Security is nearby."},
            
            # East Section
            "4,5": {"name": "East Section", "desc": "A hallway along the eastern side of the station."},
            "3,5": {"name": "East Section", "desc": "A hallway along the eastern side of the station."},
            "2,5": {"name": "East Section", "desc": "A hallway along the eastern side of the station."},
            "1,5": {"name": "East Section", "desc": "A hallway connecting back to the main hallways."},
            
            # Special Rooms (Locked)
            "6,0": {"name": "Bridge", "desc": "The control center of the station. The door is unlocked.", "locked": False},
            "0,6": {"name": "MedBay", "desc": "The medical facility of the station. The door is unlocked.", "locked": False},
            "6,6": {"name": "Security", "desc": "The security center of the station. The door is unlocked.", "locked": False},
            "6,3": {"name": "Engineering Bay", "desc": "The station's engineering and maintenance center. The door is unlocked.", "locked": False},
            "0,-1": {"name": "Bar", "desc": "The station's social hub where crew members can relax and enjoy drinks. The door is unlocked.", "locked": False}
        }
        
        # Bind the window close event to stop the market thread
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        self.show_main_menu()
    
    def on_closing(self):
        # Stop the market thread before closing
        self.stop_market_thread()
        self.root.destroy()
    
    def start_market_thread(self):
        if not self.market_running:
            self.market_running = True
            self.market_thread = threading.Thread(target=self.run_stock_market, daemon=True)
            self.market_thread.start()
    
    def stop_market_thread(self):
        self.market_running = False
        if self.market_thread and self.market_thread.is_alive():
            self.market_thread.join(1)  # Give it 1 second to finish
    
    def run_stock_market(self):
        """Run the stock market in the background"""
        while self.market_running:
            # Calculate time until next update
            now = datetime.datetime.now()
            elapsed = (now - self.last_update_time).total_seconds()
            
            # If 60 seconds have passed since last update
            if elapsed >= 60:
                # Update all companies
                for company in self.companies:
                    company.update_value()
                
                # Update cycle and day numbers
                self.stock_cycle_number += 1
                self.stock_day_number = (self.stock_cycle_number // 5) + 1
                
                # Update last update time
                self.last_update_time = now
                
                # Update player data with current market state
                self.update_market_data()
                
                # Process any pending trades if any
                self.process_pending_trades()
            
            # Sleep for 1 second before checking again
            time.sleep(1)
    
    def process_pending_trades(self):
        """Process any pending trades in the player data"""
        if "pending_trades" in self.player_data["stock_market"]:
            pending = self.player_data["stock_market"]["pending_trades"]
            if pending and (pending.get('bought') or pending.get('sold')):
                # Check if we already have a trade log for this cycle
                if "trade_log" not in self.player_data["stock_market"]:
                    self.player_data["stock_market"]["trade_log"] = []
                
                # Check if there's already an entry for the current cycle
                current_cycle_log = None
                for entry in self.player_data["stock_market"]["trade_log"]:
                    if entry.get("cycle") == self.stock_cycle_number and entry.get("day") == self.stock_day_number:
                        current_cycle_log = entry
                        break
                
                # Only create an entry if there are actual trades
                has_trades = False
                if pending.get('bought'):
                    has_trades = any(trade.get('amount', 0) > 0 for trade in pending['bought'].values())
                if not has_trades and pending.get('sold'):
                    has_trades = any(trade.get('amount', 0) > 0 for trade in pending['sold'].values())
                
                if current_cycle_log and has_trades:
                    # Update existing entry for this cycle
                    trades = current_cycle_log.get("trades", {})
                    
                    # Update bought trades
                    if 'bought' in pending:
                        if 'bought' not in trades:
                            trades['bought'] = {}
                        for company, trade_data in pending['bought'].items():
                            amount = trade_data.get('amount', 0)
                            if amount > 0:  # Only process trades with non-zero amounts
                                if company in trades['bought']:
                                    # Merge the trades
                                    trades['bought'][company]['amount'] += amount
                                    trades['bought'][company]['total'] += trade_data.get('total', 0)
                                else:
                                    # Add new company trades
                                    trades['bought'][company] = trade_data
                    
                    # Update sold trades
                    if 'sold' in pending:
                        if 'sold' not in trades:
                            trades['sold'] = {}
                        for company, trade_data in pending['sold'].items():
                            amount = trade_data.get('amount', 0)
                            if amount > 0:  # Only process trades with non-zero amounts
                                if company in trades['sold']:
                                    # Merge the trades
                                    trades['sold'][company]['amount'] += amount
                                    trades['sold'][company]['total'] += trade_data.get('total', 0)
                                else:
                                    # Add new company trades
                                    trades['sold'][company] = trade_data
                    
                    # Update the trades in the current cycle log
                    current_cycle_log["trades"] = trades
                    
                elif has_trades:
                    # Add new trade entry for this cycle
                    trade_entry = {
                        "cycle": self.stock_cycle_number,
                        "day": self.stock_day_number,
                        "trades": pending
                    }
                    self.player_data["stock_market"]["trade_log"].append(trade_entry)
                
                # Clear pending trades
                self.player_data["stock_market"]["pending_trades"] = {}
    
    def update_market_data(self):
        """Update player data with current market state"""
        # Store company data
        company_data = []
        for company in self.companies:
            company_data.append({
                "name": company.name,
                "current_value": company.current_value,
                "previous_value": company.previous_value,
                "price_history": company.price_history,
                "owned_shares": company.owned_shares if hasattr(company, "owned_shares") else 0
            })
        
        # Update player data
        self.player_data["stock_market"].update({
            "cycle_number": self.stock_cycle_number,
            "day_number": self.stock_day_number,
            "companies": company_data,
            "last_update_time": self.last_update_time.isoformat()
        })
        
        # Ensure trade log exists
        if "trade_log" not in self.player_data["stock_market"]:
            self.player_data["stock_market"]["trade_log"] = []
    
    def load_market_data(self):
        """Load market data from player data"""
        if "stock_market" in self.player_data:
            market_data = self.player_data["stock_market"]
            
            # Load cycle and day numbers
            self.stock_cycle_number = market_data.get("cycle_number", 0)
            self.stock_day_number = market_data.get("day_number", 1)
            
            # Load last update time
            if "last_update_time" in market_data:
                try:
                    self.last_update_time = datetime.datetime.fromisoformat(market_data["last_update_time"])
                except (ValueError, TypeError):
                    # If there's an error parsing the time, use current time
                    self.last_update_time = datetime.datetime.now()
            else:
                self.last_update_time = datetime.datetime.now()
            
            # Load company data
            if "companies" in market_data and len(market_data["companies"]) == len(self.companies):
                for i, company_data in enumerate(market_data["companies"]):
                    self.companies[i].name = company_data["name"]
                    self.companies[i].current_value = company_data["current_value"]
                    self.companies[i].previous_value = company_data["previous_value"]
                    self.companies[i].price_history = company_data["price_history"]
                    self.companies[i].owned_shares = company_data.get("owned_shares", 0)
    
    def get_time_until_next_update(self):
        """Calculate the time in seconds until the next market update"""
        now = datetime.datetime.now()
        elapsed = (now - self.last_update_time).total_seconds()
        remaining = max(0, 60 - elapsed)
        return int(remaining)
    
    def show_main_menu(self):
        # Stop the market thread when returning to main menu
        self.stop_market_thread()
        
        # Clear the window
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Title
        title_label = tk.Label(self.root, text="Space Station Explorer", font=("Arial", 24), bg="black", fg="white")
        title_label.pack(pady=50)
        
        # Buttons
        button_frame = tk.Frame(self.root, bg="black")
        button_frame.pack(pady=20)
        
        new_game_btn = tk.Button(button_frame, text="New Game", font=("Arial", 14), width=15, command=self.show_character_creation)
        new_game_btn.pack(pady=10)
        
        load_game_btn = tk.Button(button_frame, text="Load Game", font=("Arial", 14), width=15, command=self.show_load_game)
        load_game_btn.pack(pady=10)
        
        quit_btn = tk.Button(button_frame, text="Quit", font=("Arial", 14), width=15, command=self.on_closing)
        quit_btn.pack(pady=10)
    
    def show_character_creation(self):
        # Clear the window
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Title
        title_label = tk.Label(self.root, text="Character Creation", font=("Arial", 24), bg="black", fg="white")
        title_label.pack(pady=30)
        
        # Character creation form
        form_frame = tk.Frame(self.root, bg="black")
        form_frame.pack(pady=20)
        
        # Name input
        name_label = tk.Label(form_frame, text="Character Name:", font=("Arial", 14), bg="black", fg="white")
        name_label.grid(row=0, column=0, sticky="w", pady=10)
        
        self.name_entry = tk.Entry(form_frame, font=("Arial", 14), width=25)
        self.name_entry.grid(row=0, column=1, pady=10)
        
        # Job selection
        job_label = tk.Label(form_frame, text="Select Job:", font=("Arial", 14), bg="black", fg="white")
        job_label.grid(row=1, column=0, sticky="w", pady=10)
        
        self.job_var = tk.StringVar(value="Staff Assistant")
        
        # Updated jobs list with new roles
        jobs = ["Staff Assistant", "Engineer", "Security Guard", "Doctor", "Captain", "Bartender"]
        job_menu = tk.OptionMenu(form_frame, self.job_var, *jobs, command=self.update_job_information)
        job_menu.config(font=("Arial", 14), width=20)
        job_menu.grid(row=1, column=1, pady=10)
        
        # Credits display based on selected job
        credits_label = tk.Label(form_frame, text="Starting Credits:", font=("Arial", 14), bg="black", fg="white")
        credits_label.grid(row=2, column=0, sticky="w", pady=10)
        
        self.credits_value = tk.Label(form_frame, text="1000 cr", font=("Arial", 14), bg="black", fg="white")
        self.credits_value.grid(row=2, column=1, sticky="w", pady=10)
        
        # Job description frame
        desc_frame = tk.Frame(self.root, bg="black")
        desc_frame.pack(pady=10, fill=tk.X, padx=50)
        
        desc_label = tk.Label(desc_frame, text="Job Description:", font=("Arial", 14, "bold"), bg="black", fg="white")
        desc_label.pack(anchor=tk.W)
        
        self.job_description = tk.Label(desc_frame, text="", font=("Arial", 12), bg="black", fg="white", wraplength=700, justify=tk.LEFT)
        self.job_description.pack(anchor=tk.W, pady=5)
        
        # Initialize the job description for the default job
        self.update_job_information(self.job_var.get())
        
        # Buttons
        button_frame = tk.Frame(self.root, bg="black")
        button_frame.pack(pady=20)
        
        start_game_btn = tk.Button(button_frame, text="Start Game", font=("Arial", 14), width=15, command=self.start_game)
        start_game_btn.pack(side=tk.LEFT, padx=10)
        
        back_btn = tk.Button(button_frame, text="Back", font=("Arial", 14), width=15, command=self.show_main_menu)
        back_btn.pack(side=tk.LEFT, padx=10)
    
    def update_job_information(self, job_name):
        """Update the job description and credits display based on selected job"""
        job = job_name
        
        # Set credit amount based on job
        if job == "Staff Assistant":
            credits = 1000
            description = "Staff Assistants are the backbone of daily station operations. They handle various tasks as needed across the station. Starting with 1000 credits."
        elif job == "Engineer":
            credits = 2500
            description = "Engineers are responsible for keeping the station's critical systems operational. They excel at repairing equipment and solving technical problems. Starting with 2500 credits and access to the Engineering Station."
        elif job == "Security Guard":
            credits = 5000
            description = "Security Guards maintain order and protect the station from threats. They have access to security systems and equipment. Starting with 5000 credits and access to the Security Station."
        elif job == "Doctor":
            credits = 7500
            description = "Doctors provide medical care to the station's crew. They can diagnose and treat a variety of conditions. Starting with 7500 credits and access to the MedBay Station."
        elif job == "Captain":
            credits = 10000
            description = "The Captain is the highest authority on the station. They make critical decisions and coordinate all departments. Starting with 10000 credits and access to all station areas."
        elif job == "Bartender":
            credits = 3500
            description = "Bartenders run the station's social hub, mixing drinks and providing a place for crew members to relax. They have deep knowledge of beverages and excellent social skills. Starting with 3500 credits and access to the Bar Station."
        else:
            credits = 1000  # Default
            description = "Select a job to see its description."
            
        # Update the credits display
        self.credits_value.config(text=f"{credits} cr")
        
        # Update the job description
        self.job_description.config(text=description)
    
    def start_game(self):
        # Get player information
        player_name = self.name_entry.get().strip()
        
        if not player_name:
            messagebox.showerror("Error", "Please enter a character name.")
            return
        
        # Save player data
        self.player_data["name"] = player_name
        self.player_data["job"] = self.job_var.get()
        self.player_data["inventory"] = []
        self.player_data["location"] = {"x": 0, "y": 0}
        self.player_data["stock_holdings"] = {}
        
        # Set starting credits based on job
        job = self.job_var.get()
        if job == "Staff Assistant":
            self.player_data["credits"] = 1000
        elif job == "Engineer":
            self.player_data["credits"] = 2500
        elif job == "Security Guard":
            self.player_data["credits"] = 5000
        elif job == "Doctor":
            self.player_data["credits"] = 7500
        elif job == "Captain":
            self.player_data["credits"] = 10000
        elif job == "Bartender":
            self.player_data["credits"] = 3500
        else:
            self.player_data["credits"] = 1000  # Default for Staff Assistant
            
        # Set job-specific permissions for room access
        if job == "Captain":
            # Captain has access to all stations
            self.player_data["permissions"] = {
                "security_station": True,
                "medbay_station": True,
                "bridge_station": True,
                "engineering_station": True,
                "bar_station": True
            }
        else:
            # Other jobs have specific access
            self.player_data["permissions"] = {
                "security_station": job == "Security Guard",
                "medbay_station": job == "Doctor",
                "bridge_station": job == "Captain",
                "engineering_station": job == "Engineer",
                "bar_station": job == "Bartender"
            }
        
        # Create or save character file 
        self.save_and_start()
    
    def save_and_start(self):
        """Save the character and start the game"""
        # Update market data before saving
        self.update_market_data()
        
        # Create saves directory if it doesn't exist
        saves_path = os.path.join(self.base_path, "saves")
        os.makedirs(saves_path, exist_ok=True)
        
        # Save game to JSON file
        filename = os.path.join(saves_path, f"{self.player_data['name']}.json")
        with open(filename, "w") as f:
            json.dump(self.player_data, f, indent=4)
        
        # Initialize stock market data
        self.update_market_data()
        
        # Start the market thread
        self.start_market_thread()
        
        # Show room
        self.show_room()
    
    def show_room(self):
        # Clear the window
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Title
        room_label = tk.Label(self.root, text="Your Quarters", font=("Arial", 24), bg="black", fg="white")
        room_label.pack(pady=30)
        
        # Description
        desc_label = tk.Label(self.root, text="A small living quarters with basic amenities.", 
                             font=("Arial", 12), bg="black", fg="white", wraplength=600)
        desc_label.pack(pady=10)
        
        # Player info
        info_frame = tk.Frame(self.root, bg="black")
        info_frame.pack(pady=10)
        
        name_label = tk.Label(info_frame, text=f"Name: {self.player_data['name']}", font=("Arial", 12), bg="black", fg="white")
        name_label.pack(side=tk.LEFT, padx=20)
        
        job_label = tk.Label(info_frame, text=f"Job: {self.player_data['job']}", font=("Arial", 12), bg="black", fg="white")
        job_label.pack(side=tk.LEFT, padx=20)
        
        credits_label = tk.Label(info_frame, text=f"Credits: {self.player_data['credits']:.2f}", font=("Arial", 12), bg="black", fg="white")
        credits_label.pack(side=tk.LEFT, padx=20)
        
        # Room items
        button_frame = tk.Frame(self.root, bg="black")
        button_frame.pack(pady=20)
        
        bed_btn = tk.Button(button_frame, text="Bed", font=("Arial", 14), width=15, command=self.interact_bed)
        bed_btn.grid(row=0, column=0, padx=10, pady=10)
        
        locker_btn = tk.Button(button_frame, text="Storage Locker", font=("Arial", 14), width=15, command=self.show_storage)
        locker_btn.grid(row=0, column=1, padx=10, pady=10)
        
        computer_btn = tk.Button(button_frame, text="Computer", font=("Arial", 14), width=15, command=self.show_computer)
        computer_btn.grid(row=1, column=0, padx=10, pady=10)
        
        door_btn = tk.Button(button_frame, text="Door", font=("Arial", 14), width=15, command=self.use_door)
        door_btn.grid(row=1, column=1, padx=10, pady=10)
        
        # Character sheet button 
        character_btn = tk.Button(button_frame, text="Character Sheet", font=("Arial", 14), width=15, command=self.show_character_sheet)
        character_btn.grid(row=2, column=0, columnspan=2, padx=10, pady=10)
        
        # Save and exit button
        save_frame = tk.Frame(self.root, bg="black")
        save_frame.pack(pady=30)
        
        save_btn = tk.Button(save_frame, text="Save and Exit", font=("Arial", 14), width=15, command=self.save_and_exit)
        save_btn.pack()
    
    def show_character_sheet(self):
        """Show the character sheet window"""
        # Clear the window
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Title
        title_label = tk.Label(self.root, text="Character Sheet", font=("Arial", 24), bg="black", fg="white")
        title_label.pack(pady=20)
        
        # Character info
        info_frame = tk.Frame(self.root, bg="black")
        info_frame.pack(pady=10)
        
        # Name and job
        name_label = tk.Label(info_frame, text=f"Name: {self.player_data['name']}", font=("Arial", 14), bg="black", fg="white")
        name_label.pack(anchor="w", padx=10, pady=5)
        
        job_label = tk.Label(info_frame, text=f"Job: {self.player_data['job']}", font=("Arial", 14), bg="black", fg="white")
        job_label.pack(anchor="w", padx=10, pady=5)
        
        # Credits
        credits_label = tk.Label(info_frame, text=f"Credits: {self.player_data['credits']}", font=("Arial", 14), bg="black", fg="white")
        credits_label.pack(anchor="w", padx=10, pady=5)
        
        # Buttons for inventory, stock holdings, and notes
        button_frame = tk.Frame(info_frame, bg="black")
        button_frame.pack(anchor="w", padx=10, pady=5, fill=tk.X)
        
        # Inventory button
        inv_count = len(self.player_data.get('inventory', []))
        inv_btn = tk.Button(button_frame, text=f"View Inventory ({inv_count} items)", 
                          font=("Arial", 12), width=20, command=self.show_inventory_popup)
        inv_btn.pack(side=tk.LEFT, padx=5, pady=5)
        
        # Stock holdings button
        holdings_count = len(self.player_data.get('stock_holdings', {}))
        stock_btn = tk.Button(button_frame, text=f"View Stock Holdings ({holdings_count})", 
                            font=("Arial", 12), width=20, command=self.show_holdings_popup)
        stock_btn.pack(side=tk.LEFT, padx=5, pady=5)
        
        # Notes button
        notes_count = len(self.player_data.get('notes', []))
        notes_btn = tk.Button(button_frame, text=f"View Notes ({notes_count})", 
                            font=("Arial", 12), width=15, command=self.show_notes_popup)
        notes_btn.pack(side=tk.LEFT, padx=5, pady=5)
        
        # Limb health - horizontal layout
        limb_label = tk.Label(info_frame, text="Limb Health:", font=("Arial", 14), bg="black", fg="white")
        limb_label.pack(anchor="w", padx=10, pady=5)
        
        # Create a frame for the horizontal limb health display
        limb_frame = tk.Frame(info_frame, bg="black")
        limb_frame.pack(fill=tk.X, padx=20, pady=5)
        
        # Create a 2x3 grid for the 6 limbs
        row1_frame = tk.Frame(limb_frame, bg="black")
        row1_frame.pack(fill=tk.X, pady=2)
        
        row2_frame = tk.Frame(limb_frame, bg="black")
        row2_frame.pack(fill=tk.X, pady=2)
        
        # Sort limbs into logical order
        limb_order = ["head", "chest", "left_arm", "right_arm", "left_leg", "right_leg"]
        
        # First row: Head, Chest, Left Arm
        for i, limb_name in enumerate(limb_order[:3]):
            if limb_name in self.player_data['limbs']:
                health = self.player_data['limbs'][limb_name]
                display_name = limb_name.replace('_', ' ').title()
                
                # Change color based on health
                color = "green" if health > 75 else "yellow" if health > 40 else "red"
                
                limb_frame = tk.Frame(row1_frame, bg="black", width=200)
                limb_frame.pack(side=tk.LEFT, padx=10, expand=True)
                
                limb_health_label = tk.Label(limb_frame, text=f"{display_name}: {health}%", 
                                         font=("Arial", 12), bg="black", fg=color)
                limb_health_label.pack(side=tk.LEFT)
        
        # Second row: Right Arm, Left Leg, Right Leg
        for i, limb_name in enumerate(limb_order[3:]):
            if limb_name in self.player_data['limbs']:
                health = self.player_data['limbs'][limb_name]
                display_name = limb_name.replace('_', ' ').title()
                
                # Change color based on health
                color = "green" if health > 75 else "yellow" if health > 40 else "red"
                
                limb_frame = tk.Frame(row2_frame, bg="black", width=200)
                limb_frame.pack(side=tk.LEFT, padx=10, expand=True)
                
                limb_health_label = tk.Label(limb_frame, text=f"{display_name}: {health}%", 
                                         font=("Arial", 12), bg="black", fg=color)
                limb_health_label.pack(side=tk.LEFT)
        
        # Store the previous screen to return to
        self.previous_screen = getattr(self, 'previous_screen', 'show_room')
        
        # Return button that goes back to the previous screen
        return_btn = tk.Button(self.root, text="Return", font=("Arial", 14), width=15, 
                             command=lambda: getattr(self, self.previous_screen)())
        return_btn.pack(pady=20)
    
    def show_notes_popup(self):
        """Show a popup window with the player's notes"""
        popup = tk.Toplevel(self.root)
        popup.title("Character Notes")
        popup.geometry("600x500")
        popup.configure(bg="black")
        
        # Ensure this window stays on top
        popup.transient(self.root)
        popup.grab_set()
        
        # Center the popup window
        popup.update_idletasks()
        width = 600
        height = 500
        x = (popup.winfo_screenwidth() // 2) - (width // 2)
        y = (popup.winfo_screenheight() // 2) - (height // 2)
        popup.geometry(f"{width}x{height}+{x}+{y}")
        
        # Title
        title_label = tk.Label(popup, text="Character Notes", font=("Arial", 18), bg="black", fg="white")
        title_label.pack(pady=10)
        
        # Create a frame for the scrollable notes
        frame = tk.Frame(popup, bg="black")
        frame.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)
        
        # Add a scrollbar
        scrollbar = tk.Scrollbar(frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Create a text widget for notes
        notes_text = tk.Text(frame, bg="black", fg="white", font=("Arial", 12),
                           width=60, height=20, yscrollcommand=scrollbar.set, wrap=tk.WORD)
        notes_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=notes_text.yview)
        
        # Disable editing
        notes_text.config(state=tk.DISABLED)
        
        # Load notes
        if "notes" in self.player_data and self.player_data["notes"]:
            # Re-enable text widget temporarily to insert text
            notes_text.config(state=tk.NORMAL)
            
            # Insert notes in reverse order (newest first)
            for note in reversed(self.player_data["notes"]):
                # Format the note
                if "timestamp" in note and "text" in note:
                    timestamp = note["timestamp"]
                    text = note["text"]
                    
                    # Format the timestamp for display
                    try:
                        # Parse ISO format timestamp
                        dt = datetime.datetime.fromisoformat(timestamp)
                        formatted_time = dt.strftime("%Y-%m-%d %H:%M:%S")
                    except (ValueError, TypeError):
                        # If timestamp format is invalid, use it as is
                        formatted_time = timestamp
                    
                    # Insert the formatted note
                    notes_text.insert(tk.END, f"{formatted_time}:\n{text}\n\n")
                else:
                    # If note doesn't have proper structure, just insert the text
                    notes_text.insert(tk.END, f"{str(note)}\n\n")
            
            # Disable editing again
            notes_text.config(state=tk.DISABLED)
        else:
            # If no notes, show a message
            notes_text.config(state=tk.NORMAL)
            notes_text.insert(tk.END, "No notes recorded yet.")
            notes_text.config(state=tk.DISABLED)
        
        # Close button
        close_btn = tk.Button(popup, text="Close", font=("Arial", 12), width=10, command=popup.destroy)
        close_btn.pack(pady=10)
    
    def add_note(self, text):
        """Add a note to the player's notes"""
        if "notes" not in self.player_data:
            self.player_data["notes"] = []
        
        # Create a new note with timestamp
        note = {
            "timestamp": datetime.datetime.now().isoformat(),
            "text": text
        }
        
        # Add the note to the player's notes
        self.player_data["notes"].append(note)
    
    def show_inventory_popup(self):
        """Show a popup window with the player's inventory"""
        popup = tk.Toplevel(self.root)
        popup.title("Inventory")
        popup.geometry("400x500")  # Made taller to accommodate the read button
        popup.configure(bg="black")
        
        # Ensure this window stays on top
        popup.transient(self.root)
        popup.grab_set()
        
        # Center the popup window
        popup.update_idletasks()
        width = 400
        height = 500
        x = (popup.winfo_screenwidth() // 2) - (width // 2)
        y = (popup.winfo_screenheight() // 2) - (height // 2)
        popup.geometry(f"{width}x{height}+{x}+{y}")
        
        # Title
        title_label = tk.Label(popup, text="Inventory", font=("Arial", 18), bg="black", fg="white")
        title_label.pack(pady=10)
        
        # Create a frame for the scrollable inventory
        frame = tk.Frame(popup, bg="black")
        frame.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)
        
        # Add a scrollbar
        scrollbar = tk.Scrollbar(frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Create a listbox for inventory items
        inventory_list = tk.Listbox(frame, bg="black", fg="white", font=("Arial", 12),
                                  width=30, height=15, yscrollcommand=scrollbar.set)
        inventory_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=inventory_list.yview)
        
        # Add items to the listbox
        if not self.player_data.get('inventory', []):
            inventory_list.insert(tk.END, "Your inventory is empty.")
        else:
            for item in self.player_data['inventory']:
                inventory_list.insert(tk.END, item)
        
        # Button frame for actions
        button_frame = tk.Frame(popup, bg="black")
        button_frame.pack(pady=10)
        
        # Read button (only enabled when a readable item is selected)
        read_btn = tk.Button(button_frame, text="Read Item", font=("Arial", 12), width=10, 
                         command=lambda: self.read_book(inventory_list, popup),
                         state=tk.DISABLED)
        read_btn.pack(side=tk.LEFT, padx=5)
        
        # Close button
        close_btn = tk.Button(button_frame, text="Close", font=("Arial", 12), width=10, command=popup.destroy)
        close_btn.pack(side=tk.LEFT, padx=5)
        
        # Check if selection is a readable item
        def check_selection(event):
            selection = inventory_list.curselection()
            if selection and inventory_list.get(selection[0]) in BOOK_CONTENTS:
                read_btn.config(state=tk.NORMAL)
            else:
                read_btn.config(state=tk.DISABLED)
        
        # Bind to listbox selection
        inventory_list.bind('<<ListboxSelect>>', check_selection)
    
    def read_book(self, inventory_list, parent_popup):
        """Display the contents of a readable item"""
        selection = inventory_list.curselection()
        if not selection:
            return
        
        item_name = inventory_list.get(selection[0])
        if item_name not in BOOK_CONTENTS:
            return
        
        # Create a new window for reading
        read_popup = tk.Toplevel(parent_popup)
        read_popup.title(f"Reading: {item_name}")
        read_popup.geometry("600x500")
        read_popup.configure(bg="black")
        read_popup.transient(parent_popup)
        read_popup.grab_set()
        
        # Center the popup
        read_popup.update_idletasks()
        width = 600
        height = 500
        x = (read_popup.winfo_screenwidth() // 2) - (width // 2)
        y = (read_popup.winfo_screenheight() // 2) - (height // 2)
        read_popup.geometry(f"{width}x{height}+{x}+{y}")
        
        # Title
        title_label = tk.Label(read_popup, text=item_name, font=("Arial", 18), bg="black", fg="white")
        title_label.pack(pady=10)
        
        # Text content frame
        content_frame = tk.Frame(read_popup, bg="black")
        content_frame.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)
        
        # Add scrollbar for text
        content_scrollbar = tk.Scrollbar(content_frame)
        content_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Text widget for content
        content_text = tk.Text(content_frame, bg="black", fg="white", font=("Arial", 12),
                             wrap=tk.WORD, yscrollcommand=content_scrollbar.set)
        content_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        content_scrollbar.config(command=content_text.yview)
        
        # Insert book content
        content_text.insert(tk.END, BOOK_CONTENTS[item_name])
        content_text.config(state=tk.DISABLED)  # Make read-only
        
        # Add note that player read the book
        self.add_note(f"Read the {item_name}.")
        
        # Close button
        close_btn = tk.Button(read_popup, text="Close", font=("Arial", 12), width=10, command=read_popup.destroy)
        close_btn.pack(pady=10)
    
    def show_holdings_popup(self):
        """Show a popup window with the player's stock holdings"""
        popup = tk.Toplevel(self.root)
        popup.title("Stock Holdings")
        popup.geometry("400x400")
        popup.configure(bg="black")
        
        # Ensure this window stays on top
        popup.transient(self.root)
        popup.grab_set()
        
        # Center the popup window
        popup.update_idletasks()
        width = 400
        height = 400
        x = (popup.winfo_screenwidth() // 2) - (width // 2)
        y = (popup.winfo_screenheight() // 2) - (height // 2)
        popup.geometry(f"{width}x{height}+{x}+{y}")
        
        # Title
        title_label = tk.Label(popup, text="Stock Holdings", font=("Arial", 18), bg="black", fg="white")
        title_label.pack(pady=10)
        
        # Create a frame for the scrollable holdings list
        frame = tk.Frame(popup, bg="black")
        frame.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)
        
        # Add a scrollbar
        scrollbar = tk.Scrollbar(frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Create a listbox for holdings
        holdings_list = tk.Listbox(frame, bg="black", fg="white", font=("Arial", 12),
                                 width=30, height=15, yscrollcommand=scrollbar.set)
        holdings_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=holdings_list.yview)
        
        # Add holdings to the listbox
        if not self.player_data.get('stock_holdings', {}):
            holdings_list.insert(tk.END, "You don't own any company stocks.")
        else:
            for company, shares in self.player_data['stock_holdings'].items():
                holdings_list.insert(tk.END, f"{company}: {shares} shares")
        
        # Close button
        close_btn = tk.Button(popup, text="Close", font=("Arial", 12), width=10, command=popup.destroy)
        close_btn.pack(pady=10)
    
    def interact_bed(self):
        # Create a new top-level window for save dialog
        save_window = tk.Toplevel(self.root)
        save_window.title("Bed")
        save_window.geometry("300x150")
        save_window.transient(self.root)
        save_window.grab_set()
        
        # Center the window
        save_window.geometry("+%d+%d" % (self.root.winfo_rootx() + 250,
                                        self.root.winfo_rooty() + 200))
        
        # Create frame with padding
        save_frame = tk.Frame(save_window, bg="black")
        save_frame.pack(fill=tk.BOTH, expand=True)
        
        # Message
        tk.Label(
            save_frame,
            text="Would you like to save your game?",
            font=("Arial", 12),
            bg="black",
            fg="white"
        ).pack(pady=10)
        
        # Buttons frame
        buttons_frame = tk.Frame(save_frame, bg="black")
        buttons_frame.pack(pady=10)
        
        # Yes button
        tk.Button(
            buttons_frame,
            text="Yes",
            font=("Arial", 12),
            command=lambda: self.save_game_and_close(save_window)
        ).pack(side=tk.LEFT, padx=10)
        
        # No button
        tk.Button(
            buttons_frame,
            text="No",
            font=("Arial", 12),
            command=save_window.destroy
        ).pack(side=tk.LEFT, padx=10)
    
    def save_game_and_close(self, save_window):
        """Save the game and close the save dialog"""
        # Update market data before saving
        self.update_market_data()
        
        # Create saves directory if it doesn't exist
        saves_path = os.path.join(self.base_path, "saves")
        os.makedirs(saves_path, exist_ok=True)
        
        # Save game to JSON file
        filename = os.path.join(saves_path, f"{self.player_data['name']}.json")
        with open(filename, "w") as f:
            json.dump(self.player_data, f, indent=4)
        
        # Close the save dialog without showing a confirmation
        save_window.destroy()
    
    def show_storage(self):
        # Clear the window
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Title
        storage_label = tk.Label(self.root, text="Storage Locker", font=("Arial", 24), bg="black", fg="white")
        storage_label.pack(pady=20)
        
        # Container for locker and inventory sections
        main_container = tk.Frame(self.root, bg="black")
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Left frame for locker items
        locker_frame = tk.LabelFrame(main_container, text="Locker Items", font=("Arial", 14), bg="black", fg="white", bd=2)
        locker_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Right frame for player inventory
        inventory_frame = tk.LabelFrame(main_container, text="Your Inventory", font=("Arial", 14), bg="black", fg="white", bd=2)
        inventory_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Locker items data - ensure all readable books are included
        locker_items = [
            {"name": "Welcome Guide", "description": "A guide for new station personnel"},
            {"name": "Flashlight", "description": "A standard issue flashlight"},
            {"name": "Station Map", "description": "A digital map of the station"},
            {"name": "Emergency Rations", "description": "Standard emergency food supply"},
            {"name": "Basic Tools", "description": "A set of basic maintenance tools"},
            {"name": "ID Card Reader", "description": "Device to read crew ID cards"},
            {"name": "Portable Scanner", "description": "Handheld scanner for analyzing objects"},
            {"name": "Maintenance Manual", "description": "Guide for basic station repairs"},
            {"name": "Emergency Beacon", "description": "Distress signal device for emergencies"},
            {"name": "First Aid Kit", "description": "Basic medical supplies for minor injuries"}
        ]
        
        # Filter out items already in inventory
        filtered_items = [item for item in locker_items if item["name"] not in self.player_data["inventory"]]
        
        # Create scrollable canvas for locker items
        locker_canvas = tk.Canvas(locker_frame, bg="black", highlightthickness=0)
        locker_scrollbar = tk.Scrollbar(locker_frame, orient="vertical", command=locker_canvas.yview)
        
        # Configure the canvas
        locker_canvas.configure(yscrollcommand=locker_scrollbar.set)
        locker_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        locker_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Create a frame inside the canvas to hold the items
        locker_items_frame = tk.Frame(locker_canvas, bg="black")
        locker_canvas.create_window((0, 0), window=locker_items_frame, anchor="nw")
        
        # Populate locker items frame
        if not filtered_items:
            empty_label = tk.Label(locker_items_frame, text="The storage locker is empty.", font=("Arial", 12), bg="black", fg="white")
            empty_label.pack(pady=10, padx=10, anchor="w")
        else:
            for i, item in enumerate(filtered_items):
                item_frame = tk.Frame(locker_items_frame, bg="dark gray", bd=2, relief=tk.RAISED, width=300)
                item_frame.pack(fill=tk.X, pady=5, padx=5)
                
                # Item info
                info_frame = tk.Frame(item_frame, bg="dark gray")
                info_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, anchor="w")
                
                item_name = tk.Label(info_frame, text=item["name"], font=("Arial", 12, "bold"), bg="dark gray")
                item_name.pack(anchor="w", padx=10, pady=(5, 0))
                
                item_desc = tk.Label(info_frame, text=item["description"], font=("Arial", 10), bg="dark gray", wraplength=200)
                item_desc.pack(anchor="w", padx=10, pady=(0, 5))
                
                # Take button on the right
                button_frame = tk.Frame(item_frame, bg="dark gray")
                button_frame.pack(side=tk.RIGHT, padx=10, pady=5)
                
                take_btn = tk.Button(button_frame, text="Take", font=("Arial", 10),
                                    command=lambda i=item["name"]: self.take_item(i))
                take_btn.pack()
        
        # Create scrollable canvas for inventory items
        inventory_canvas = tk.Canvas(inventory_frame, bg="black", highlightthickness=0)
        inventory_scrollbar = tk.Scrollbar(inventory_frame, orient="vertical", command=inventory_canvas.yview)
        
        # Configure the canvas
        inventory_canvas.configure(yscrollcommand=inventory_scrollbar.set)
        inventory_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        inventory_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Create a frame inside the canvas to hold the items
        inventory_items_frame = tk.Frame(inventory_canvas, bg="black")
        inventory_canvas.create_window((0, 0), window=inventory_items_frame, anchor="nw")
        
        # Populate inventory items
        if not self.player_data["inventory"]:
            empty_label = tk.Label(inventory_items_frame, text="Your inventory is empty.", font=("Arial", 12), bg="black", fg="white")
            empty_label.pack(pady=10, padx=10, anchor="w")
        else:
            for i, item in enumerate(self.player_data["inventory"]):
                item_frame = tk.Frame(inventory_items_frame, bg="dark gray", bd=2, relief=tk.RAISED, width=300)
                item_frame.pack(fill=tk.X, pady=5, padx=5)
                
                # Item info - just the name for inventory items
                name_label = tk.Label(item_frame, text=item, font=("Arial", 12, "bold"), bg="dark gray")
                name_label.pack(side=tk.LEFT, padx=10, pady=5, anchor="w")
                
                # Store button on the right
                store_btn = tk.Button(item_frame, text="Store in Locker", font=("Arial", 10),
                                    command=lambda i=item: self.store_item(i))
                store_btn.pack(side=tk.RIGHT, padx=10, pady=5)
        
        # Configure the canvas to scroll properly
        locker_items_frame.update_idletasks()
        locker_canvas.config(scrollregion=locker_canvas.bbox("all"))
        
        inventory_items_frame.update_idletasks()
        inventory_canvas.config(scrollregion=inventory_canvas.bbox("all"))
        
        # Mouse wheel scrolling
        locker_canvas.bind_all("<MouseWheel>", lambda event: self._on_mousewheel(event, locker_canvas))
        inventory_canvas.bind_all("<MouseWheel>", lambda event: self._on_mousewheel(event, inventory_canvas))
        
        # Back button
        back_btn = tk.Button(self.root, text="Back to Room", font=("Arial", 14), width=15, command=self.show_room)
        back_btn.pack(pady=20)
    
    def _on_mousewheel(self, event, canvas):
        """Handle mouse wheel scrolling"""
        canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    
    def take_item(self, item_name):
        if item_name not in self.player_data["inventory"]:
            self.player_data["inventory"].append(item_name)
            messagebox.showinfo("Item Taken", f"You took the {item_name}.")
            self.show_storage()  # Refresh the storage view
        else:
            messagebox.showinfo("Already Taken", f"You already have the {item_name}.")
    
    def store_item(self, item_name):
        if item_name in self.player_data["inventory"]:
            self.player_data["inventory"].remove(item_name)
            messagebox.showinfo("Item Stored", f"You placed the {item_name} in the storage locker.")
            self.show_storage()  # Refresh the storage view
    
    def show_computer(self):
        # Clear the window
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Title
        computer_label = tk.Label(self.root, text="Computer Terminal", font=("Arial", 24), bg="black", fg="white")
        computer_label.pack(pady=30)
        
        # Computer options
        options_frame = tk.Frame(self.root, bg="black")
        options_frame.pack(pady=20)
        
        stock_btn = tk.Button(options_frame, text="Stock Market", font=("Arial", 14), width=15,
                             command=self.open_stock_market)
        stock_btn.pack(pady=10)
        
        turnoff_btn = tk.Button(options_frame, text="Turn Off Computer", font=("Arial", 14), width=15, command=self.show_room)
        turnoff_btn.pack(pady=10)
    
    def open_stock_market(self):
        # Calculate time until next update
        time_until_update = self.get_time_until_next_update()
        
        # Pass the current market state to the stock market window
        market = StockMarket(self.root, self.player_data, self.companies, 
                           self.stock_cycle_number, self.stock_day_number, self.update_player_data)
    
    def update_player_data(self, updated_data):
        # Update player data when returning from stock market
        
        # Check if there were any stock transactions
        if "stock_transactions" in updated_data:
            transactions = updated_data.pop("stock_transactions")
            
            # Log notes for significant transactions
            for transaction in transactions:
                if transaction["type"] == "buy":
                    self.add_note(f"Bought {transaction['shares']} shares of {transaction['company']} at {transaction['price']:.2f} cr/share (Total: {transaction['total']:.2f} cr)")
                elif transaction["type"] == "sell":
                    profit = transaction.get("profit", 0)
                    if profit != 0:
                        profit_text = f" (Profit: {profit:.2f} cr)" if profit > 0 else f" (Loss: {abs(profit):.2f} cr)"
                    else:
                        profit_text = ""
                    
                    self.add_note(f"Sold {transaction['shares']} shares of {transaction['company']} at {transaction['price']:.2f} cr/share (Total: {transaction['total']:.2f} cr){profit_text}")
        
        self.player_data = updated_data
        
        # Update owned shares in the companies list
        if "stock_holdings" in updated_data:
            for company in self.companies:
                company.owned_shares = updated_data["stock_holdings"].get(company.name, 0)
        
        # Return to computer menu instead of room view
        self.show_computer()
    
    def use_door(self):
        # Set initial location when leaving quarters
        self.player_data["location"] = {"x": 0, "y": 0}
        self.show_hallway()
    
    def get_location_key(self):
        x = self.player_data["location"]["x"]
        y = self.player_data["location"]["y"]
        return f"{x},{y}"
    
    def show_hallway(self):
        # Clear the window
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Get current location
        loc_key = self.get_location_key()
        
        if loc_key not in self.ship_map:
            messagebox.showerror("Error", "Invalid location!")
            self.player_data["location"] = {"x": 0, "y": 0}
            loc_key = "0,0"
        
        # Check if we're at a special room that can be entered
        if self.check_special_room():
            return
        
        location = self.ship_map[loc_key]
        
        # Check if room is locked
        if location.get("locked", False):
            messagebox.showinfo("Locked Door", f"The door to the {location['name']} is locked. You need proper authorization to enter.")
            # Return to previous position
            prev_x, prev_y = self.get_previous_position()
            self.player_data["location"]["x"] = prev_x
            self.player_data["location"]["y"] = prev_y
            # Show hallway again with updated position
            self.show_hallway()
            return
        
        # Title
        hallway_label = tk.Label(self.root, text=location["name"], font=("Arial", 24), bg="black", fg="white")
        hallway_label.pack(pady=30)
        
        # Description
        desc_label = tk.Label(self.root, text=location["desc"], 
                             font=("Arial", 12), bg="black", fg="white", wraplength=600)
        desc_label.pack(pady=10)
        
        # Location info
        coords_label = tk.Label(self.root, text=f"Location: {self.player_data['location']['x']} North, {self.player_data['location']['y']} East", 
                             font=("Arial", 10), bg="black", fg="white")
        coords_label.pack(pady=5)
        
        # Navigation buttons
        nav_frame = tk.Frame(self.root, bg="black")
        nav_frame.pack(pady=20)
        
        # Determine available directions
        x = self.player_data["location"]["x"]
        y = self.player_data["location"]["y"]
        
        # Add an unlock door button if appropriate
        if self.is_near_special_room():
            unlock_btn = tk.Button(self.root, text="Unlock Door", font=("Arial", 14), width=15,
                               command=self.unlock_door)
            unlock_btn.pack(pady=10)
        
        # Updated movement logic for circuit and locked rooms:
        north_available = False
        south_available = False
        east_available = False
        west_available = False
        
        # Standard hallway directions
        # North hallway section (0-5, 0)
        if y == 0 and x < 5:
            north_available = True
        if y == 0 and x > 0:
            south_available = True
            
        # East hallway section (0, 0-5)
        if x == 0 and y < 5:
            east_available = True
        if x == 0 and y > 0:
            west_available = True
            
        # North end - can go east
        if x == 5 and y < 5:
            east_available = True
        if x == 5 and y > 0:
            west_available = True
            
        # East end - can go north
        if y == 5 and x < 5:
            north_available = True
        if y == 5 and x > 0:
            south_available = True
        
        # Special cases for room access points
        is_special_location = False
        
        # Bridge access from north end
        if x == 5 and y == 0:
            is_special_location = True
            # Add the Bridge access button
            bridge_btn = tk.Button(nav_frame, text="Bridge", font=("Arial", 14), width=15,
                                command=lambda: self.enter_special_room_at("Bridge", "6,0"))
            bridge_btn.grid(row=0, column=1, padx=10, pady=10)
            
            # Also add regular east button for the corridor
            if east_available:
                east_btn = tk.Button(nav_frame, text="Go East", font=("Arial", 14), width=15,
                                   command=lambda: self.move_direction("east"))
                east_btn.grid(row=1, column=2, padx=10, pady=10)
                
            # Add south button for returning to the corridor
            if south_available:
                south_btn = tk.Button(nav_frame, text="Go South", font=("Arial", 14), width=15,
                                    command=lambda: self.move_direction("south"))
                south_btn.grid(row=2, column=1, padx=10, pady=10)
            
        # MedBay access from east end
        elif x == 0 and y == 5:
            is_special_location = True
            # Add MedBay access button
            medbay_btn = tk.Button(nav_frame, text="MedBay", font=("Arial", 14), width=15,
                              command=lambda: self.enter_special_room_at("MedBay", "0,6"))
            medbay_btn.grid(row=1, column=2, padx=10, pady=10)
            
            # Add north button for the corridor
            if north_available:
                north_btn = tk.Button(nav_frame, text="Go North", font=("Arial", 14), width=15,
                                    command=lambda: self.move_direction("north"))
                north_btn.grid(row=0, column=1, padx=10, pady=10)
                
            # Add west button for returning to the corridor
            if west_available:
                west_btn = tk.Button(nav_frame, text="Go West", font=("Arial", 14), width=15,
                                   command=lambda: self.move_direction("west"))
                west_btn.grid(row=1, column=0, padx=10, pady=10)
            
        # Security access from northeast corner
        elif x == 5 and y == 5:
            is_special_location = True
            # Just one button for Security access
            security_btn = tk.Button(nav_frame, text="Security", font=("Arial", 14), width=15,
                                 command=lambda: self.enter_special_room_at("Security", "6,6"))
            security_btn.grid(row=0, column=1, padx=10, pady=10)
            
            # Add west and south buttons for the corridors
            west_btn = tk.Button(nav_frame, text="Go West", font=("Arial", 14), width=15,
                               command=lambda: self.move_direction("west"))
            west_btn.grid(row=1, column=0, padx=10, pady=10)
            
            south_btn = tk.Button(nav_frame, text="Go South", font=("Arial", 14), width=15,
                                command=lambda: self.move_direction("south"))
            south_btn.grid(row=2, column=1, padx=10, pady=10)

        # Engineering Bay access from engineering hallway
        elif x == 5 and y == 3:
            is_special_location = True
            # Add Engineering Bay access button
            eng_bay_btn = tk.Button(nav_frame, text="Engineering Bay", font=("Arial", 14), width=15,
                                command=lambda: self.enter_special_room_at("Engineering", "6,3"))
            eng_bay_btn.grid(row=0, column=1, padx=10, pady=10)
            
            # Add west and east buttons for the corridors
            west_btn = tk.Button(nav_frame, text="Go West", font=("Arial", 14), width=15,
                               command=lambda: self.move_direction("west"))
            west_btn.grid(row=1, column=0, padx=10, pady=10)
            
            east_btn = tk.Button(nav_frame, text="Go East", font=("Arial", 14), width=15,
                               command=lambda: self.move_direction("east"))
            east_btn.grid(row=1, column=2, padx=10, pady=10)
        
        # Bar access from bar entrance
        elif x == 0 and y == 3:
            is_special_location = True
            # Add Bar access button
            bar_btn = tk.Button(nav_frame, text="Bar", font=("Arial", 14), width=15,
                             command=lambda: self.enter_special_room_at("Bar", "0,-1"))
            bar_btn.grid(row=0, column=1, padx=10, pady=10)
            
            # Add west and east buttons for the corridors
            west_btn = tk.Button(nav_frame, text="Go West", font=("Arial", 14), width=15,
                               command=lambda: self.move_direction("west"))
            west_btn.grid(row=1, column=0, padx=10, pady=10)
            
            east_btn = tk.Button(nav_frame, text="Go East", font=("Arial", 14), width=15,
                               command=lambda: self.move_direction("east"))
            east_btn.grid(row=1, column=2, padx=10, pady=10)
        
        # Regular directional buttons for other hallway positions
        if not is_special_location:
            if north_available:
                north_btn = tk.Button(nav_frame, text="Go North", font=("Arial", 14), width=15,
                                    command=lambda: self.move_direction("north"))
                north_btn.grid(row=0, column=1, padx=10, pady=10)
                
            if south_available:
                south_btn = tk.Button(nav_frame, text="Go South", font=("Arial", 14), width=15,
                                    command=lambda: self.move_direction("south"))
                south_btn.grid(row=2, column=1, padx=10, pady=10)
                
            if east_available:
                east_btn = tk.Button(nav_frame, text="Go East", font=("Arial", 14), width=15,
                                   command=lambda: self.move_direction("east"))
                east_btn.grid(row=1, column=2, padx=10, pady=10)
                
            if west_available:
                west_btn = tk.Button(nav_frame, text="Go West", font=("Arial", 14), width=15,
                                   command=lambda: self.move_direction("west"))
                west_btn.grid(row=1, column=0, padx=10, pady=10)
        
        # Only show return to quarters at the starting junction
        if x == 0 and y == 0:
            quarters_btn = tk.Button(nav_frame, text="Return to Quarters", font=("Arial", 14), width=15,
                                   command=self.show_room)
            quarters_btn.grid(row=3, column=1, columnspan=1, padx=10, pady=20)
        
        # Character sheet button
        character_btn = tk.Button(self.root, text="Character Sheet", font=("Arial", 14), width=15, 
                                command=self.show_character_sheet_hallway)
        character_btn.pack(pady=10)
        
        # Save button
        save_btn = tk.Button(self.root, text="Save and Exit", font=("Arial", 14), width=15,
                          command=self.save_and_exit)
        save_btn.pack(pady=10)
    
    def show_character_sheet_hallway(self):
        # Set the previous screen to hallway before showing character sheet
        self.previous_screen = "show_hallway"
        
        # Show character sheet
        self.show_character_sheet()
    
    def move_direction(self, direction):
        """Move in the specified direction with random event chance"""
        x = self.player_data["location"]["x"]
        y = self.player_data["location"]["y"]
        
        if direction == "north":
            x += 1
        elif direction == "south":
            x -= 1
        elif direction == "east":
            y += 1
        elif direction == "west":
            y -= 1
        
        # Update location
        self.player_data["location"]["x"] = x
        self.player_data["location"]["y"] = y
        
        # Log for debugging
        print(f"Moving to location: {x},{y}")
        
        # Check if the destination exists in the ship map
        loc_key = f"{x},{y}"
        if loc_key not in self.ship_map:
            # For Security specifically, it needs a different handling from Northeast Corner
            if x == 6 and y == 5 and self.ship_map.get("6,6", {}).get("name") == "Security":
                # For the Security special case, jump directly to the security location
                self.player_data["location"]["x"] = 6
                self.player_data["location"]["y"] = 6
            # Special case for Engineering Bay entrance
            elif x == 5 and y == 3:
                # This is handled by the check_special_room method
                pass
            else:
                # Otherwise, revert to previous location for invalid moves
                messagebox.showerror("Error", "You can't go that way!")
                self.player_data["location"]["x"] = x - (1 if direction == "north" else -1 if direction == "south" else 0)
                self.player_data["location"]["y"] = y - (1 if direction == "east" else -1 if direction == "west" else 0)
        
        # Random event check (40% chance) when moving through hallways
        if random.random() < 0.20:  # Changed from 0.40 to 0.20 (20% chance)
            self.trigger_random_event()
        
        # Refresh hallway view
        self.show_hallway()
    
    def trigger_random_event(self):
        """Trigger a random event"""
        # List of possible events with good, bad, and neutral outcomes
        events = [
            # Good events
            {"type": "good", "title": "Found Credits", "desc": "You found some credits on the floor!", "effect": lambda: self.add_credits(random.randint(50, 200))},
            {"type": "good", "title": "Supply Crate", "desc": "You found an unsealed supply crate with useful items.", "effect": lambda: self.add_random_item()},
            {"type": "good", "title": "Market Tip", "desc": "You overheard a reliable market tip.", "effect": lambda: self.add_market_knowledge()},
            
            # Neutral events
            {"type": "neutral", "title": "Crew Member", "desc": "You passed by a crew member who nodded at you.", "effect": lambda: None},
            {"type": "neutral", "title": "Announcement", "desc": "The station PA system makes an announcement.", "effect": lambda: self.station_announcement()},
            {"type": "neutral", "title": "Maintenance", "desc": "A maintenance drone passes by, cleaning the hallway.", "effect": lambda: None},
            
            # Bad events
            {"type": "bad", "title": "Lost Credits", "desc": "You dropped some credits and couldn't find them all.", "effect": lambda: self.lose_credits(random.randint(10, 50))},
            {"type": "bad", "title": "Small Explosion", "desc": "A nearby conduit explodes, showering you with hot sparks!", "effect": lambda: self.damage_random_limb(10, 25)},
            {"type": "bad", "title": "Slip and Fall", "desc": "You slipped on a wet floor and fell hard.", "effect": lambda: self.damage_random_limb(5, 15)},
            {"type": "bad", "title": "Steam Leak", "desc": "A pipe bursts, releasing scalding steam that burns your arm!", "effect": lambda: self.damage_limb("left_arm", 10, 30)},
            {"type": "bad", "title": "Falling Debris", "desc": "A ceiling panel breaks loose and hits your head!", "effect": lambda: self.damage_limb("head", 15, 35)},
            {"type": "bad", "title": "Maintenance Accident", "desc": "Your leg gets caught in an open floor grate!", "effect": lambda: self.damage_limb("right_leg", 10, 20)}
        ]
        
        # Pick a random event
        event = random.choice(events)
        
        # Show the event
        messagebox.showinfo(event["title"], event["desc"])
        
        # Apply the effect
        event["effect"]()
    
    def damage_random_limb(self, min_damage, max_damage):
        """Damage a random limb by a random amount"""
        # Get a random limb
        limb = random.choice(list(self.player_data["limbs"].keys()))
        self.damage_limb(limb, min_damage, max_damage)
    
    def damage_limb(self, limb, min_damage, max_damage):
        """Damage a specific limb by a random amount within range"""
        if limb in self.player_data["limbs"]:
            # Calculate damage
            damage = random.randint(min_damage, max_damage)
            
            # Apply damage
            original_health = self.player_data["limbs"][limb]
            self.player_data["limbs"][limb] = max(0, original_health - damage)
            
            # Format the limb name for display
            limb_name = limb.replace('_', ' ').title()
            
            # Show damage message
            messagebox.showinfo("Injury", f"Your {limb_name} took {damage}% damage and is now at {self.player_data['limbs'][limb]}%.")
            
            # Add note about the injury
            self.add_note(f"Injured {limb_name}: Took {damage}% damage (from {original_health}% to {self.player_data['limbs'][limb]}%)")
    
    def add_credits(self, amount):
        """Add credits to the player"""
        self.player_data["credits"] += amount
        messagebox.showinfo("Credits Added", f"You gained {amount} credits.")
        
        # Add note about credits gained
        self.add_note(f"Found {amount} credits. New balance: {self.player_data['credits']} credits.")
    
    def lose_credits(self, amount):
        """Subtract credits from the player (min 0)"""
        old_credits = self.player_data["credits"]
        self.player_data["credits"] = max(0, old_credits - amount)
        messagebox.showinfo("Credits Lost", f"You lost {amount} credits.")
        
        # Add note about credits lost
        self.add_note(f"Lost {amount} credits. New balance: {self.player_data['credits']} credits.")
    
    def show_load_game(self):
        # Clear the window
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Title
        load_label = tk.Label(self.root, text="Load Game", font=("Arial", 24), bg="black", fg="white")
        load_label.pack(pady=30)
        
        # Check if saves directory exists
        saves_path = os.path.join(self.base_path, "saves")
        os.makedirs(saves_path, exist_ok=True)
        
        # Get save files
        save_files = [f for f in os.listdir(saves_path) if f.endswith(".json")]
        
        if not save_files:
            no_saves_label = tk.Label(self.root, text="No saved games found.", font=("Arial", 14), bg="black", fg="white")
            no_saves_label.pack(pady=20)
        else:
            saves_frame = tk.Frame(self.root, bg="black")
            saves_frame.pack(pady=20)
            
            for save_file in save_files:
                # Strip .json extension for display
                player_name = save_file[:-5]
                
                save_btn = tk.Button(saves_frame, text=player_name, font=("Arial", 14), width=20,
                                     command=lambda file=save_file: self.load_game(file))
                save_btn.pack(pady=5)
        
        # Back button
        back_btn = tk.Button(self.root, text="Back", font=("Arial", 14), width=15, command=self.show_main_menu)
        back_btn.pack(pady=20)
    
    def load_game(self, save_file):
        try:
            saves_path = os.path.join(self.base_path, "saves")
            with open(os.path.join(saves_path, save_file), "r") as f:
                self.player_data = json.load(f)
            
            # Load market data
            self.load_market_data()
            
            # Start the market thread
            self.start_market_thread()
            
            # Check if player was in hallway when saved
            if "location" in self.player_data and (self.player_data["location"]["x"] > 0 or self.player_data["location"]["y"] > 0):
                self.show_hallway()
            else:
                # Default to quarters if location not specified or at origin
                if "location" not in self.player_data:
                    self.player_data["location"] = {"x": 0, "y": 0}
                self.show_room()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load game: {str(e)}")
    
    def get_previous_position(self):
        """Get the previous position before entering a locked room"""
        x = self.player_data["location"]["x"]
        y = self.player_data["location"]["y"]
        
        # Bridge entrance (6,0) -> return to North End (5,0)
        if x == 6 and y == 0:
            return 5, 0
            
        # MedBay entrance (0,6) -> return to East End (0,5)
        if x == 0 and y == 6:
            return 0, 5
            
        # Security entrance (6,6) -> return to Northeast Corner (5,5)
        if x == 6 and y == 6:
            return 5, 5
            
        # Engineering Bay entrance (6,3) -> return to Engineering Bay Entrance (5,3)
        if x == 6 and y == 3:
            return 5, 3
            
        # Bar entrance (0,-1) -> return to Bar Entrance (0,3)
        if x == 0 and y == -1:
            return 0, 3
        
        # Default to junction if something goes wrong
        return 0, 0

    def enter_special_room(self, room_name):
        """Enter a special room on the station"""
        # Import special room classes
        from game.special_rooms import MedBay, Bridge, Security, Engineering, Bar
        from game.quarters import Quarters
        
        # Add the ship_map to player_data for special rooms to access
        self.player_data["ship_map"] = self.ship_map
        
        if room_name == "MedBay":
            # Open MedBay
            medbay = MedBay(self.root, self.player_data, self.update_player_data_from_room)
        elif room_name == "Bridge":
            # Open Bridge
            bridge = Bridge(self.root, self.player_data, self.update_player_data_from_room)
        elif room_name == "Security":
            # Open Security
            security = Security(self.root, self.player_data, self.update_player_data_from_room)
        elif room_name == "Engineering":
            # Open Engineering Bay
            engineering = Engineering(self.root, self.player_data, self.update_player_data_from_room)
        elif room_name == "Bar":
            # Open Bar
            bar = Bar(self.root, self.player_data, self.update_player_data_from_room)
        elif room_name == "Quarters":
            # Return to quarters
            quarters = Quarters(self.root, self.player_data, self.update_player_data_from_room)
    
    def update_player_data_from_room(self, updated_data):
        """Update player data when returning from a room"""
        # Update player data
        self.player_data = updated_data
        
        # Return to the previous position in the hallway
        # (not the room position, which causes loops)
        x = self.player_data["location"]["x"]
        y = self.player_data["location"]["y"]
        
        # If we're in a special room, move back to the previous position
        if (x == 6 and y == 0) or (x == 0 and y == 6) or (x == 6 and y == 6) or (x == 6 and y == 3) or (x == 0 and y == -1):
            # For Engineering Bay specifically, return to the hallway entrance
            if x == 6 and y == 3:
                self.player_data["location"]["x"] = 5
                self.player_data["location"]["y"] = 3
            # For Bar specifically, return to the hallway entrance
            elif x == 0 and y == -1:
                self.player_data["location"]["x"] = 0
                self.player_data["location"]["y"] = 3
            else:
                prev_x, prev_y = self.get_previous_position()
                self.player_data["location"]["x"] = prev_x
                self.player_data["location"]["y"] = prev_y
        
        # Update ship_map if it was modified in the special room
        if "ship_map" in self.player_data:
            self.ship_map = self.player_data["ship_map"]
            # Remove it from player_data to keep it clean
            del self.player_data["ship_map"]
        
        # Show hallway screen
        self.show_hallway()

    def unlock_door(self):
        """Attempt to unlock a special room door"""
        x = self.player_data["location"]["x"]
        y = self.player_data["location"]["y"]
        location_key = f"{x},{y}"
        
        # Check if there's an adjacent special room to unlock
        special_rooms = {
            "5,0": "Bridge",     # Adjacent to Bridge
            "0,5": "MedBay",     # Adjacent to MedBay
            "5,5": "Security",   # Adjacent to Security
            "5,3": "Engineering", # Adjacent to Engineering
            "0,3": "Bar"         # Adjacent to Bar
        }
        
        if location_key in special_rooms:
            room_name = special_rooms[location_key]
            room_coords = {
                "Bridge": "6,0", 
                "MedBay": "0,6", 
                "Security": "6,6",
                "Engineering": "6,3",
                "Bar": "0,-1"
            }
            room_key = room_coords[room_name]
            
            # Check if room is locked
            if self.ship_map[room_key].get("locked", False):
                # Unlock the room
                self.ship_map[room_key]["locked"] = False
                self.ship_map[room_key]["desc"] = f"The {room_name}. The door is unlocked."
                
                # Don't change the player's location, just open the room
                self.enter_special_room(room_name)
            else:
                # Room is already unlocked, just enter it
                self.enter_special_room(room_name)
        else:
            messagebox.showinfo("No Door Nearby", "There's no special room door nearby to unlock.")

    def check_special_room(self):
        """Check if we're at a special room and can enter it"""
        x = self.player_data["location"]["x"]
        y = self.player_data["location"]["y"]
        location_key = f"{x},{y}"
        
        # Define special room coordinates and their names
        special_rooms = {
            "6,0": "Bridge",
            "0,6": "MedBay",
            "6,6": "Security"
        }
        
        if location_key in special_rooms:
            room_name = special_rooms[location_key]
            
            # If room is not locked, allow entry
            if not self.ship_map[location_key].get("locked", False):
                # Enter the special room
                self.enter_special_room(room_name)
                return True
            else:
                messagebox.showinfo("Locked Door", f"The {room_name} door is locked.")
        
        return False

    def is_near_special_room(self):
        """Check if we're near a special room that can be unlocked"""
        x = self.player_data["location"]["x"]
        y = self.player_data["location"]["y"]
        location_key = f"{x},{y}"
        
        # Adjacent locations to special rooms
        special_room_adjacents = {
            "5,0": "Bridge",     # Adjacent to Bridge
            "0,5": "MedBay",     # Adjacent to MedBay
            "5,5": "Security",   # Adjacent to Security
            "5,3": "Engineering", # Adjacent to Engineering Bay
            "0,3": "Bar"         # Adjacent to Bar
        }
        
        # Check if we're near a special room and if that room is locked
        if location_key in special_room_adjacents:
            room_name = special_room_adjacents[location_key]
            room_coords = {
                "Bridge": "6,0", 
                "MedBay": "0,6", 
                "Security": "6,6",
                "Engineering": "6,3",
                "Bar": "0,-1"
            }
            room_key = room_coords[room_name]
            
            # Only return True if the room is actually locked
            return self.ship_map[room_key].get("locked", False)
            
        return False

    def enter_special_room_at(self, room_name, target_key):
        """Enter a special room at a specified target location"""
        # Check if the room is locked
        if self.ship_map[target_key].get("locked", False):
            messagebox.showinfo("Locked Door", f"The {room_name} door is locked. You need to unlock it first.")
            return
        
        # Store current position before entering room
        current_x = self.player_data["location"]["x"]
        current_y = self.player_data["location"]["y"]
        
        # Navigate to the target location temporarily
        self.player_data["location"]["x"] = int(target_key.split(",")[0])
        self.player_data["location"]["y"] = int(target_key.split(",")[1])
        
        # Add the ship_map to player_data for special rooms to access
        self.player_data["ship_map"] = self.ship_map
        
        # Import special room classes
        from game.special_rooms import MedBay, Bridge, Security, Engineering, Bar
        from game.quarters import Quarters
        
        # Open the appropriate room
        if room_name == "MedBay":
            medbay = MedBay(self.root, self.player_data, self.update_player_data_from_room)
        elif room_name == "Bridge":
            bridge = Bridge(self.root, self.player_data, self.update_player_data_from_room)
        elif room_name == "Security":
            security = Security(self.root, self.player_data, self.update_player_data_from_room)
        elif room_name == "Engineering":
            engineering = Engineering(self.root, self.player_data, self.update_player_data_from_room)
        elif room_name == "Bar":
            bar = Bar(self.root, self.player_data, self.update_player_data_from_room)
        elif room_name == "Quarters":
            quarters = Quarters(self.root, self.player_data, self.update_player_data_from_room)

    def save_and_exit(self):
        """Save the game and exit to main menu"""
        # Update market data before saving
        self.update_market_data()
        
        # Create saves directory if it doesn't exist
        saves_path = os.path.join(self.base_path, "saves")
        os.makedirs(saves_path, exist_ok=True)
        
        # Save game to JSON file
        filename = os.path.join(saves_path, f"{self.player_data['name']}.json")
        with open(filename, "w") as f:
            json.dump(self.player_data, f, indent=4)
        
        # Stop the market thread
        self.stop_market_thread()
        
        # Return to main menu
        self.show_main_menu()

    def add_random_item(self):
        """Add a random item to the player's inventory"""
        items = [
            "Medkit",
            "Repair Tool",
            "Flashlight",
            "Energy Bar",
            "Circuit Board",
            "Battery Pack",
            "ID Card",
            "Data Pad",
            "Oxygen Canister",
            "Radiation Badge",
            "Maintenance Tool",
            "Security Pass",
            "Medical Scanner",
            "Communication Device",
            "Power Cell",
            "Stabilizing Agent",
            "Diagnostic Tool",
            "Engineering Manual",
            "Security Keycard",
            "Medical Supply Kit",
            "Emergency Flare",
            "Navigation Chart",
            "Encrypted Data Drive"
        ]
        item = random.choice(items)
        
        if "inventory" not in self.player_data:
            self.player_data["inventory"] = []
            
        self.player_data["inventory"].append(item)
        messagebox.showinfo("Item Found", f"You found a {item} and added it to your inventory.")
        
        # Add note about the item found
        self.add_note(f"Found {item} and added it to inventory.")
    
    def add_market_knowledge(self):
        """Add market knowledge to the player - reveals a tip about a stock"""
        if not self.player_data["stock_market"]["companies"]:
            messagebox.showinfo("Market Tip", "You heard a stock tip, but don't understand the market yet.")
            return
            
        company = random.choice(self.player_data["stock_market"]["companies"])
        direction = random.choice(["rise", "fall"])
        
        message = ""
        if direction == "rise":
            message = f"Overheard that {company['name']} stock is expected to rise soon!"
            messagebox.showinfo("Market Tip", message)
        else:
            message = f"Overheard that {company['name']} stock might be dropping in value soon!"
            messagebox.showinfo("Market Tip", message)
        
        # Add note about the market tip
        self.add_note(f"Market Tip: {message}")
    
    def station_announcement(self):
        """Display a random station announcement"""
        announcements = [
            "Reminder to all crew: safety protocols must be followed at all times.",
            "The cafeteria will be serving special meal rations today.",
            "Maintenance is scheduled in Sector 7 tomorrow.",
            "All personnel are reminded to report suspicious activity to security.",
            "Weekly crew meeting is postponed until further notice.",
            "Environmental controls are being recalibrated. Expect minor temperature fluctuations."
        ]
        
        announcement = random.choice(announcements)
        messagebox.showinfo("Station Announcement", f"The PA system crackles: '{announcement}'")

if __name__ == "__main__":
    root = tk.Tk()
    app = SpaceStationGame(root)
    root.mainloop() 