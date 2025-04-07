import tkinter as tk
import json
import os
import time
import threading
import datetime
from tkinter import messagebox
from tkinter import simpledialog

# Add the stock market imports
import random
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

# Import the StockMarket class
from game.stock_market import StockMarket
from game.stock_market import Company

class SpaceStationGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Space Station Explorer")
        self.root.geometry("800x600")
        self.root.configure(bg="black")
        
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
            }
        }
        
        # Ship map configuration - Updated to include locked rooms
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
            "0,3": {"name": "East Hallway", "desc": "A long hallway stretching east."},
            "0,4": {"name": "East Hallway", "desc": "A long hallway stretching east."},
            "0,5": {"name": "East End", "desc": "The eastern end of the hallway. The medbay is nearby."},
            
            # Northeast Corridors
            "5,1": {"name": "Northeast Hallway", "desc": "A hallway connecting the north and east corridors."},
            "5,2": {"name": "Northeast Hallway", "desc": "A hallway connecting the north and east corridors."},
            "5,3": {"name": "Northeast Hallway", "desc": "A hallway connecting the north and east corridors."},
            "5,4": {"name": "Northeast Hallway", "desc": "A hallway connecting the north and east corridors."},
            "5,5": {"name": "Northeast Corner", "desc": "The far corner of the station. Security is nearby."},
            
            # East Section
            "4,5": {"name": "East Section", "desc": "A hallway along the eastern side of the station."},
            "3,5": {"name": "East Section", "desc": "A hallway along the eastern side of the station."},
            "2,5": {"name": "East Section", "desc": "A hallway along the eastern side of the station."},
            "1,5": {"name": "East Section", "desc": "A hallway connecting back to the main hallways."},
            
            # Special Rooms (Locked)
            "6,0": {"name": "Bridge", "desc": "The control center of the station. The door is locked.", "locked": True},
            "0,6": {"name": "MedBay", "desc": "The medical facility of the station. The door is locked.", "locked": True},
            "6,6": {"name": "Security", "desc": "The security center of the station. The door is locked.", "locked": True}
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
        job_menu = tk.OptionMenu(form_frame, self.job_var, "Staff Assistant")
        job_menu.config(font=("Arial", 14), width=20)
        job_menu.grid(row=1, column=1, pady=10)
        
        # Credits display
        credits_label = tk.Label(form_frame, text="Starting Credits:", font=("Arial", 14), bg="black", fg="white")
        credits_label.grid(row=2, column=0, sticky="w", pady=10)
        
        credits_value = tk.Label(form_frame, text=f"{self.player_data['credits']} cr", font=("Arial", 14), bg="black", fg="white")
        credits_value.grid(row=2, column=1, sticky="w", pady=10)
        
        # Buttons
        button_frame = tk.Frame(self.root, bg="black")
        button_frame.pack(pady=30)
        
        start_game_btn = tk.Button(button_frame, text="Start Game", font=("Arial", 14), width=15, command=self.start_game)
        start_game_btn.pack(side=tk.LEFT, padx=10)
        
        back_btn = tk.Button(button_frame, text="Back", font=("Arial", 14), width=15, command=self.show_main_menu)
        back_btn.pack(side=tk.LEFT, padx=10)
    
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
        # Clear the window
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Title
        char_label = tk.Label(self.root, text="Character Sheet", font=("Arial", 24), bg="black", fg="white")
        char_label.pack(pady=30)
        
        # Character info frame
        info_frame = tk.Frame(self.root, bg="black")
        info_frame.pack(pady=20, fill=tk.X, padx=50)
        
        # Name
        name_label = tk.Label(info_frame, text="Name:", font=("Arial", 14, "bold"), bg="black", fg="white")
        name_label.grid(row=0, column=0, sticky="w", pady=5)
        name_value = tk.Label(info_frame, text=self.player_data["name"], font=("Arial", 14), bg="black", fg="white")
        name_value.grid(row=0, column=1, sticky="w", pady=5)
        
        # Job
        job_label = tk.Label(info_frame, text="Job:", font=("Arial", 14, "bold"), bg="black", fg="white")
        job_label.grid(row=1, column=0, sticky="w", pady=5)
        job_value = tk.Label(info_frame, text=self.player_data["job"], font=("Arial", 14), bg="black", fg="white")
        job_value.grid(row=1, column=1, sticky="w", pady=5)
        
        # Credits
        credits_label = tk.Label(info_frame, text="Credits:", font=("Arial", 14, "bold"), bg="black", fg="white")
        credits_label.grid(row=2, column=0, sticky="w", pady=5)
        credits_value = tk.Label(info_frame, text=f"{self.player_data['credits']:.2f}", font=("Arial", 14), bg="black", fg="white")
        credits_value.grid(row=2, column=1, sticky="w", pady=5)
        
        # Inventory
        inv_label = tk.Label(self.root, text="Inventory", font=("Arial", 18, "bold"), bg="black", fg="white")
        inv_label.pack(pady=(20, 10))
        
        inv_frame = tk.Frame(self.root, bg="black")
        inv_frame.pack(pady=10, fill=tk.BOTH, expand=True, padx=50)
        
        if not self.player_data["inventory"]:
            empty_label = tk.Label(inv_frame, text="Your inventory is empty.", font=("Arial", 14), bg="black", fg="white")
            empty_label.pack(pady=10)
        else:
            for i, item in enumerate(self.player_data["inventory"]):
                item_frame = tk.Frame(inv_frame, bg="dark gray", bd=2, relief=tk.RAISED)
                item_frame.pack(fill=tk.X, pady=5)
                
                item_name = tk.Label(item_frame, text=item, font=("Arial", 12), bg="dark gray")
                item_name.pack(side=tk.LEFT, anchor="w", padx=10, pady=5)
        
        # Back button
        back_btn = tk.Button(self.root, text="Back", font=("Arial", 14), width=15, command=self.show_room)
        back_btn.pack(pady=20)
    
    def interact_bed(self):
        messagebox.showinfo("Bed", "Not time to sleep.")
    
    def show_storage(self):
        # Clear the window
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Title
        storage_label = tk.Label(self.root, text="Storage Locker", font=("Arial", 24), bg="black", fg="white")
        storage_label.pack(pady=30)
        
        # Items
        items_frame = tk.Frame(self.root, bg="black")
        items_frame.pack(pady=20)
        
        locker_items = [
            {"name": "Welcome Guide", "description": "A guide for new station personnel"},
            {"name": "Flashlight", "description": "A standard issue flashlight"},
            {"name": "Station Map", "description": "A digital map of the station"}
        ]
        
        # Filter out items already in inventory
        filtered_items = [item for item in locker_items if item["name"] not in self.player_data["inventory"]]
        
        if not filtered_items:
            empty_label = tk.Label(items_frame, text="The storage locker is empty.", font=("Arial", 14), bg="black", fg="white")
            empty_label.pack(pady=10)
        else:
            for i, item in enumerate(filtered_items):
                item_frame = tk.Frame(items_frame, bg="dark gray", bd=2, relief=tk.RAISED)
                item_frame.pack(fill=tk.X, padx=20, pady=5)
                
                item_name = tk.Label(item_frame, text=item["name"], font=("Arial", 12, "bold"), bg="dark gray")
                item_name.pack(anchor="w", padx=10, pady=5)
                
                item_desc = tk.Label(item_frame, text=item["description"], font=("Arial", 10), bg="dark gray")
                item_desc.pack(anchor="w", padx=10, pady=2)
                
                take_btn = tk.Button(item_frame, text="Take", 
                                    command=lambda i=item["name"]: self.take_item(i))
                take_btn.pack(anchor="e", padx=10, pady=5)
        
        # Player inventory section - for returning items to locker
        if self.player_data["inventory"]:
            inv_label = tk.Label(self.root, text="Your Inventory", font=("Arial", 18), bg="black", fg="white")
            inv_label.pack(pady=(20, 10))
            
            inv_frame = tk.Frame(self.root, bg="black")
            inv_frame.pack(pady=10)
            
            for i, item in enumerate(self.player_data["inventory"]):
                item_frame = tk.Frame(inv_frame, bg="dark gray", bd=2, relief=tk.RAISED)
                item_frame.pack(fill=tk.X, padx=20, pady=5)
                
                item_name = tk.Label(item_frame, text=item, font=("Arial", 12, "bold"), bg="dark gray")
                item_name.pack(side=tk.LEFT, padx=10, pady=5)
                
                store_btn = tk.Button(item_frame, text="Store in Locker", 
                                     command=lambda i=item: self.store_item(i))
                store_btn.pack(side=tk.RIGHT, padx=10, pady=5)
        
        # Back button
        back_btn = tk.Button(self.root, text="Back to Room", font=("Arial", 14), width=15, command=self.show_room)
        back_btn.pack(pady=20)
    
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
                                command=lambda: self.move_direction("north"))
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
                              command=lambda: self.move_direction("east"))
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
                                 command=lambda: self.move_to_security())
            security_btn.grid(row=0, column=1, padx=10, pady=10)
            
            # Add west and south buttons for the corridors
            west_btn = tk.Button(nav_frame, text="Go West", font=("Arial", 14), width=15,
                               command=lambda: self.move_direction("west"))
            west_btn.grid(row=1, column=0, padx=10, pady=10)
            
            south_btn = tk.Button(nav_frame, text="Go South", font=("Arial", 14), width=15,
                                command=lambda: self.move_direction("south"))
            south_btn.grid(row=2, column=1, padx=10, pady=10)
        
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
        # Show character sheet and then return to hallway instead of room
        self.show_character_sheet()
        
        # Override the back button functionality
        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Button) and widget["text"] == "Back":
                widget.config(command=self.show_hallway)
    
    def move_direction(self, direction):
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
            else:
                # Otherwise, revert to previous location for invalid moves
                messagebox.showerror("Error", "You can't go that way!")
                self.player_data["location"]["x"] = x - (1 if direction == "north" else -1 if direction == "south" else 0)
                self.player_data["location"]["y"] = y - (1 if direction == "east" else -1 if direction == "west" else 0)
        
        # Refresh hallway view
        self.show_hallway()
    
    def move_to_security(self):
        """Special handler for moving to Security room"""
        # Set location directly to Security room coordinates
        self.player_data["location"]["x"] = 6
        self.player_data["location"]["y"] = 6
        # Refresh hallway view
        self.show_hallway()
    
    def save_and_exit(self):
        # Update market data before saving
        self.update_market_data()
        
        # Create saves directory if it doesn't exist
        if not os.path.exists("game/saves"):
            os.makedirs("game/saves")
        
        # Save game to JSON file
        filename = f"game/saves/{self.player_data['name']}.json"
        with open(filename, "w") as f:
            json.dump(self.player_data, f, indent=4)
        
        messagebox.showinfo("Game Saved", f"Game saved as {filename}")
        self.show_main_menu()
    
    def show_load_game(self):
        # Clear the window
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Title
        load_label = tk.Label(self.root, text="Load Game", font=("Arial", 24), bg="black", fg="white")
        load_label.pack(pady=30)
        
        # Check if saves directory exists
        if not os.path.exists("game/saves"):
            os.makedirs("game/saves")
        
        # Get save files
        save_files = [f for f in os.listdir("game/saves") if f.endswith(".json")]
        
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
            with open(f"game/saves/{save_file}", "r") as f:
                self.player_data = json.load(f)
            
            # Load market data
            self.load_market_data()
            
            # Start the market thread
            self.start_market_thread()
            
            messagebox.showinfo("Game Loaded", f"Loaded game for {self.player_data['name']}")
            
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
        
        # Default to junction if something goes wrong
        return 0, 0

if __name__ == "__main__":
    root = tk.Tk()
    app = SpaceStationGame(root)
    root.mainloop() 