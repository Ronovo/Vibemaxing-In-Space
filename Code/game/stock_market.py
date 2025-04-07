import random
import tkinter as tk
from tkinter import ttk
import time
import datetime
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

class Company:
    def __init__(self, name, initial_value):
        self.name = name
        self.current_value = initial_value
        self.previous_value = initial_value
        self.label = None
        self.value_label = None
        self.owned_shares = 0
        self.shares_label = None
        self.minus_button = None
        self.plus_button = None
        self.price_history = [initial_value]  # Track price history
        self.graph_button = None

    def update_value(self):
        self.previous_value = self.current_value
        
        # Define price thresholds
        LOW_THRESHOLD = 75.0
        HIGH_THRESHOLD = 1100.0
        
        # Base probabilities for different types of changes
        base_prob = random.random()
        
        # Adjust probabilities based on current price
        if self.current_value < LOW_THRESHOLD:
            # More likely to increase when price is low
            increase_prob = 0.65
            decrease_prob = 0.35
        elif self.current_value > HIGH_THRESHOLD:
            # More likely to decrease when price is high
            increase_prob = 0.35
            decrease_prob = 0.65
        else:
            # Balanced probabilities for middle range
            increase_prob = 0.5
            decrease_prob = 0.5

        # Determine if price will increase or decrease
        will_increase = base_prob < increase_prob

        # Determine the magnitude of change
        if base_prob < 0.05:  # 5% chance for mega swing
            change_percent = random.uniform(-0.25, 0.25)
        elif base_prob < 0.15:  # 10% chance for large swing
            change_percent = random.uniform(-0.15, 0.15)
        else:  # 85% chance for normal movement
            change_percent = random.uniform(-0.10, 0.10)

        # Apply the change
        if will_increase:
            self.current_value *= (1 + abs(change_percent))
        else:
            self.current_value *= (1 - abs(change_percent))

        # Ensure price doesn't go below $1
        self.current_value = max(1.0, self.current_value)
        
        # Add to price history
        self.price_history.append(self.current_value)
        # Keep only last 20 values
        if len(self.price_history) > 20:
            self.price_history.pop(0)

class StockMarket:
    def __init__(self, parent_window, player_data, companies, cycle_number, day_number, return_callback):
        # Create a new toplevel window
        self.stock_window = tk.Toplevel(parent_window)
        self.stock_window.title("Space Station Stock Market")
        self.stock_window.geometry("1400x600")
        
        # Store parent window and return callback
        self.parent_window = parent_window
        self.return_callback = return_callback
        
        # Store player data reference
        self.player_data = player_data
        
        # Use the provided companies instead of creating new ones
        self.companies = companies
        
        # Use the provided cycle and day numbers
        self.cycle_number = cycle_number
        self.day_number = day_number
        
        # Initialize timer values
        self.after_id = None
        
        # Calculate time until next update based on last update time
        self.time_left = self.calculate_time_left()
        
        # Bind the window closing event
        self.stock_window.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Set player cash from player credits
        self.player_cash = self.player_data["credits"]
        self.player_name = self.player_data["name"]
        
        # Create cycle-based trade tracking
        self.current_cycle_trades = {}
        
        # Initialize holdings from player data
        if "stock_holdings" not in self.player_data:
            self.player_data["stock_holdings"] = {}
            
        for company in self.companies:
            company.owned_shares = self.player_data["stock_holdings"].get(company.name, 0)

        # Create main frame
        self.main_frame = ttk.Frame(self.stock_window, padding="5")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Configure grid weights
        self.stock_window.grid_rowconfigure(0, weight=1)
        self.stock_window.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(1, weight=1)
        self.main_frame.grid_columnconfigure(2, weight=1)
        self.main_frame.grid_rowconfigure(0, weight=1)

        # Left side - Market View
        self.market_frame = ttk.LabelFrame(self.main_frame, text="Market View", padding="2")
        self.market_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=2)
        self.market_frame.grid_rowconfigure(2, weight=1)

        # Create day and cycle counter label
        self.day_cycle_label = ttk.Label(
            self.market_frame,
            text=f'Day {self.day_number} | Market Cycle {(self.cycle_number % 5) + 1}',
            font=('Arial', 10, 'bold')
        )
        self.day_cycle_label.grid(row=0, column=0, columnspan=2, pady=5)

        # Create countdown timer label
        self.timer_label = ttk.Label(
            self.market_frame,
            text=f'Time until next market update: {self.time_left} seconds',
            font=('Arial', 10, 'bold')
        )
        self.timer_label.grid(row=1, column=0, columnspan=2, pady=5)

        # Create standard UI elements (company view, player controls, etc.)
        self.setup_ui()
        
        # Start the timer and UI refresh
        self.start_timer()
        self.refresh_ui()
        
        # Update buttons initial state
        self.update_buttons()
        
        # Load trade log
        self.display_trade_log()

    def setup_ui(self):
        """Setup all UI elements"""
        # Create company frame with scrollbar
        self.company_frame = ttk.Frame(self.market_frame)
        self.company_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.company_frame.grid_rowconfigure(0, weight=1)

        # Create canvas and scrollbar for market view
        self.canvas = tk.Canvas(self.company_frame, width=350)
        self.scrollbar = ttk.Scrollbar(self.company_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw", width=350)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Pack the scrollbar and canvas
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

        # Create company labels for market view
        for i, company in enumerate(self.companies):
            # Company name and current value
            company.label = ttk.Label(
                self.scrollable_frame,
                text=f"{company.name}:",
                font=('Arial', 9)
            )
            company.label.grid(row=i, column=0, sticky=tk.W, padx=2, pady=3)

            # Current value
            company.value_label = ttk.Label(
                self.scrollable_frame,
                text=f"${company.current_value:.2f} (Prev: ${company.previous_value:.2f})",
                font=('Arial', 9)
            )
            company.value_label.grid(row=i, column=1, sticky=tk.W, padx=2, pady=3)
            
            # Color based on change
            if company.current_value > company.previous_value:
                company.value_label.config(foreground="green")
            elif company.current_value < company.previous_value:
                company.value_label.config(foreground="red")

            # Graph button
            company.graph_button = ttk.Button(
                self.scrollable_frame,
                text="📈",
                command=lambda c=company: self.show_price_graph(c)
            )
            company.graph_button.grid(row=i, column=2, sticky=tk.W, padx=2, pady=3)

        # Middle side - Player Controls
        self.player_frame = ttk.LabelFrame(self.main_frame, text="Player Controls", padding="2")
        self.player_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=2)
        self.player_frame.grid_rowconfigure(2, weight=1)

        # Player name display
        self.name_frame = ttk.Frame(self.player_frame)
        self.name_frame.grid(row=0, column=0, columnspan=3, pady=2)
        
        # Display player name
        ttk.Label(
            self.name_frame,
            text=f"Player: {self.player_name}",
            font=('Arial', 9, 'bold')
        ).grid(row=0, column=0, columnspan=3, pady=2)

        # Player cash display
        self.cash_label = ttk.Label(
            self.player_frame,
            text=f"Credits: ${self.player_cash:.2f}",
            font=('Arial', 10, 'bold')
        )
        self.cash_label.grid(row=1, column=0, columnspan=3, pady=5)

        # Create player's stock controls
        self.player_stocks_frame = ttk.Frame(self.player_frame)
        self.player_stocks_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.player_stocks_frame.grid_rowconfigure(0, weight=1)

        # Create canvas and scrollbar for player stocks
        self.player_canvas = tk.Canvas(self.player_stocks_frame, width=450)
        self.player_scrollbar = ttk.Scrollbar(self.player_stocks_frame, orient="vertical", command=self.player_canvas.yview)
        self.player_scrollable_frame = ttk.Frame(self.player_canvas)

        self.player_scrollable_frame.bind(
            "<Configure>",
            lambda e: self.player_canvas.configure(scrollregion=self.player_canvas.bbox("all"))
        )

        self.player_canvas.create_window((0, 0), window=self.player_scrollable_frame, anchor="nw", width=450)
        self.player_canvas.configure(yscrollcommand=self.player_scrollbar.set)

        # Pack the scrollbar and canvas
        self.player_scrollbar.pack(side="right", fill="y")
        self.player_canvas.pack(side="left", fill="both", expand=True)

        # Create stock controls for each company
        for i, company in enumerate(self.companies):
            # Control frame for all elements
            control_frame = ttk.Frame(self.player_scrollable_frame)
            control_frame.grid(row=i, column=0, sticky=tk.E, padx=5, pady=3)

            # Company name
            ttk.Label(
                control_frame,
                text=company.name,
                font=('Arial', 9),
                width=15
            ).pack(side=tk.LEFT, padx=(0, 10))

            # Minus buttons frame
            minus_frame = ttk.Frame(control_frame)
            minus_frame.pack(side=tk.LEFT, padx=2)
            
            # Minus 100 button
            company.minus_100_button = ttk.Button(
                minus_frame,
                text="-100",
                command=lambda c=company: self.sell_stock(c, 100),
                width=6
            )
            company.minus_100_button.pack(side=tk.LEFT, padx=1)

            # Minus 10 button
            company.minus_10_button = ttk.Button(
                minus_frame,
                text="-10",
                command=lambda c=company: self.sell_stock(c, 10),
                width=5
            )
            company.minus_10_button.pack(side=tk.LEFT, padx=1)

            # Minus button
            company.minus_button = ttk.Button(
                minus_frame,
                text="-",
                command=lambda c=company: self.sell_stock(c),
                width=3
            )
            company.minus_button.pack(side=tk.LEFT, padx=1)

            # Shares owned
            company.shares_label = ttk.Label(
                control_frame,
                text=str(company.owned_shares),
                width=6,
                anchor="center"
            )
            company.shares_label.pack(side=tk.LEFT, padx=2)

            # Plus buttons frame
            plus_frame = ttk.Frame(control_frame)
            plus_frame.pack(side=tk.LEFT, padx=2)

            # Plus button
            company.plus_button = ttk.Button(
                plus_frame,
                text="+",
                command=lambda c=company: self.buy_stock(c),
                width=3
            )
            company.plus_button.pack(side=tk.LEFT, padx=1)

            # Plus 10 button
            company.plus_10_button = ttk.Button(
                plus_frame,
                text="+10",
                command=lambda c=company: self.buy_stock(c, 10),
                width=5
            )
            company.plus_10_button.pack(side=tk.LEFT, padx=1)

            # Plus 100 button
            company.plus_100_button = ttk.Button(
                plus_frame,
                text="+100",
                command=lambda c=company: self.buy_stock(c, 100),
                width=6
            )
            company.plus_100_button.pack(side=tk.LEFT, padx=1)

        # Configure column weights for the scrollable frame
        self.player_scrollable_frame.grid_columnconfigure(0, weight=1)

        # Right side - Trade Log
        self.trade_log_frame = ttk.LabelFrame(self.main_frame, text="Trade Log", padding="2")
        self.trade_log_frame.grid(row=0, column=2, sticky=(tk.W, tk.E, tk.N, tk.S), padx=2)
        self.trade_log_frame.grid_rowconfigure(1, weight=1)

        # Create trade log display with scrollbar
        self.trade_log_canvas = tk.Canvas(self.trade_log_frame, width=350)
        self.trade_log_scrollbar = ttk.Scrollbar(self.trade_log_frame, orient="vertical", command=self.trade_log_canvas.yview)
        self.trade_log_scrollable_frame = ttk.Frame(self.trade_log_canvas)

        self.trade_log_scrollable_frame.bind(
            "<Configure>",
            lambda e: self.trade_log_canvas.configure(scrollregion=self.trade_log_canvas.bbox("all"))
        )

        self.trade_log_canvas.create_window((0, 0), window=self.trade_log_scrollable_frame, anchor="nw", width=350)
        self.trade_log_canvas.configure(yscrollcommand=self.trade_log_scrollbar.set)

        # Pack the scrollbar and canvas for trade log
        self.trade_log_scrollbar.pack(side="right", fill="y")
        self.trade_log_canvas.pack(side="left", fill="both", expand=True)
        
        # Add exit button at the bottom
        self.exit_frame = ttk.Frame(self.main_frame)
        self.exit_frame.grid(row=1, column=0, columnspan=3, pady=10)
        
        self.exit_button = ttk.Button(
            self.exit_frame,
            text="Exit Stock Market",
            command=self.on_closing
        )
        self.exit_button.pack()

    def calculate_time_left(self):
        """Calculate time until next market update based on last update time"""
        if "stock_market" in self.player_data and "last_update_time" in self.player_data["stock_market"]:
            try:
                # Parse the ISO format datetime
                last_update = datetime.fromisoformat(self.player_data["stock_market"]["last_update_time"])
                
                # Calculate elapsed time in seconds
                now = datetime.now()
                elapsed = (now - last_update).total_seconds()
                
                # Calculate remaining time (60 seconds cycle)
                remaining = max(0, 60 - (elapsed % 60))
                return int(remaining)
            except (ValueError, TypeError):
                # If there's an error parsing the time, use default
                return 60
        else:
            # Default to 60 seconds if no last update time
            return 60

    def display_trade_log(self):
        """Display trade log from player data based on cycles"""
        # Clear existing trade log first
        for widget in self.trade_log_scrollable_frame.winfo_children():
            widget.destroy()
            
        # Initialize cycle trade log if it doesn't exist
        if "cycle_trade_log" not in self.player_data:
            self.player_data["cycle_trade_log"] = {}
        
        # Get trade log from player data
        cycle_trades = self.player_data["cycle_trade_log"]
        
        if not cycle_trades:
            # Display a "no trades" message
            no_trades_label = ttk.Label(
                self.trade_log_scrollable_frame,
                text="No trade history yet.",
                font=('Arial', 10)
            )
            no_trades_label.pack(pady=20)
            return
            
        # Display trades in reverse chronological order (newest first)
        # Sort by day and cycle
        sorted_cycles = sorted(cycle_trades.items(), 
                               key=lambda x: (int(x[1]["day"]), int(x[1]["cycle"])), 
                               reverse=True)
        
        for cycle_key, cycle_data in sorted_cycles:
            # Create a frame for this cycle
            cycle_frame = ttk.Frame(self.trade_log_scrollable_frame)
            cycle_frame.pack(fill=tk.X, padx=5, pady=5)
            
            # Cycle header (cycle and day)
            displayed_cycle = (cycle_data["cycle"] % 5) + 1  # Convert to 1-5 display
            header_label = ttk.Label(
                cycle_frame,
                text=f"Day {cycle_data['day']} | Cycle {displayed_cycle}",
                font=('Arial', 10, 'bold')
            )
            header_label.pack(anchor=tk.W)
            
            # No trades for this cycle
            if not cycle_data["trades"]:
                no_trades_label = ttk.Label(
                    cycle_frame,
                    text="No trades during this cycle.",
                    font=('Arial', 9)
                )
                no_trades_label.pack(anchor=tk.W, padx=10)
                continue
                
            # Process each company's trades
            for company, trade_data in cycle_data["trades"].items():
                # Buy transactions
                if trade_data["buy"]["amount"] > 0:
                    avg_price = trade_data["buy"]["total_cost"] / trade_data["buy"]["amount"]
                    buy_label = ttk.Label(
                        cycle_frame,
                        text=f"Bought {trade_data['buy']['amount']} shares of {company} at avg. ${avg_price:.2f}/share",
                        font=('Arial', 9),
                        wraplength=300
                    )
                    buy_label.pack(anchor=tk.W, padx=10)
                    
                    total_cost_label = ttk.Label(
                        cycle_frame,
                        text=f"Total spent: ${trade_data['buy']['total_cost']:.2f}",
                        font=('Arial', 9),
                        foreground="red"
                    )
                    total_cost_label.pack(anchor=tk.W, padx=20)
                
                # Sell transactions
                if trade_data["sell"]["amount"] > 0:
                    avg_price = trade_data["sell"]["total_revenue"] / trade_data["sell"]["amount"]
                    sell_label = ttk.Label(
                        cycle_frame,
                        text=f"Sold {trade_data['sell']['amount']} shares of {company} at avg. ${avg_price:.2f}/share",
                        font=('Arial', 9),
                        wraplength=300
                    )
                    sell_label.pack(anchor=tk.W, padx=10)
                    
                    total_revenue_label = ttk.Label(
                        cycle_frame,
                        text=f"Total received: ${trade_data['sell']['total_revenue']:.2f}",
                        font=('Arial', 9),
                        foreground="green"
                    )
                    total_revenue_label.pack(anchor=tk.W, padx=20)
            
            # Separator
            ttk.Separator(self.trade_log_scrollable_frame, orient='horizontal').pack(fill=tk.X, padx=5, pady=5)

    def start_timer(self):
        """Start the countdown timer"""
        self.update_timer()
    
    def update_timer(self):
        """Update the countdown timer every second"""
        # Update timer display
        self.timer_label.config(text=f'Time until next market update: {self.time_left} seconds')
        
        # Decrease time counter
        if self.time_left > 0:
            self.time_left -= 1
            # Schedule next timer update in 1 second
            self.after_id = self.stock_window.after(1000, self.update_timer)
        else:
            # When timer hits zero, add current cycle trades to log if any exist
            self.finalize_cycle_trades()
            
            # Reset timer to 60 seconds
            self.time_left = 60
            # Schedule next timer update
            self.after_id = self.stock_window.after(1000, self.update_timer)

    def buy_stock(self, company, amount=1):
        if self.player_cash >= company.current_value * amount:
            company.owned_shares += amount
            self.player_cash -= company.current_value * amount
            company.shares_label.config(text=str(company.owned_shares))
            self.cash_label.config(text=f"Credits: ${self.player_cash:.2f}")
            
            # Update player credits and holdings
            self.player_data["credits"] = self.player_cash
            self.player_data["stock_holdings"][company.name] = company.owned_shares
            
            # Track the trade for this cycle
            self.track_cycle_trade(company.name, "buy", amount, company.current_value)
            
            # Update UI
            self.update_buttons()

    def sell_stock(self, company, amount=1):
        if company.owned_shares >= amount:
            company.owned_shares -= amount
            self.player_cash += company.current_value * amount
            company.shares_label.config(text=str(company.owned_shares))
            self.cash_label.config(text=f"Credits: ${self.player_cash:.2f}")
            
            # Update player credits and holdings
            self.player_data["credits"] = self.player_cash
            self.player_data["stock_holdings"][company.name] = company.owned_shares
            
            # Track the trade for this cycle
            self.track_cycle_trade(company.name, "sell", amount, company.current_value)
            
            # Update UI
            self.update_buttons()

    def track_cycle_trade(self, company_name, action, amount, price):
        """Track trades for the current cycle, to be logged at cycle end"""
        cycle_key = f"{self.day_number}_{self.cycle_number}"
        
        if cycle_key not in self.current_cycle_trades:
            self.current_cycle_trades[cycle_key] = {}
            
        if company_name not in self.current_cycle_trades[cycle_key]:
            self.current_cycle_trades[cycle_key][company_name] = {
                "buy": {"amount": 0, "total_cost": 0},
                "sell": {"amount": 0, "total_revenue": 0}
            }
            
        if action == "buy":
            self.current_cycle_trades[cycle_key][company_name]["buy"]["amount"] += amount
            self.current_cycle_trades[cycle_key][company_name]["buy"]["total_cost"] += amount * price
        else:  # sell
            self.current_cycle_trades[cycle_key][company_name]["sell"]["amount"] += amount
            self.current_cycle_trades[cycle_key][company_name]["sell"]["total_revenue"] += amount * price

    def finalize_cycle_trades(self):
        """Add all trades from the current cycle to the log"""
        cycle_key = f"{self.day_number}_{self.cycle_number}"
        
        if cycle_key in self.current_cycle_trades and self.current_cycle_trades[cycle_key]:
            # Initialize trade log if it doesn't exist
            if "cycle_trade_log" not in self.player_data:
                self.player_data["cycle_trade_log"] = {}
                
            # Create a log entry for this cycle if it doesn't exist
            if cycle_key not in self.player_data["cycle_trade_log"]:
                self.player_data["cycle_trade_log"][cycle_key] = {
                    "day": self.day_number,
                    "cycle": self.cycle_number,
                    "trades": {},
                    "timestamp": datetime.now().isoformat()
                }
                
            # Add the trades to the log
            for company, trade_data in self.current_cycle_trades[cycle_key].items():
                self.player_data["cycle_trade_log"][cycle_key]["trades"][company] = trade_data
                
            # Clear the current cycle trades
            self.current_cycle_trades = {}
            
            # Update the trade log display
            self.display_trade_log()

    def update_buttons(self):
        for company in self.companies:
            company.minus_button.config(state='normal' if company.owned_shares > 0 else 'disabled')
            company.minus_10_button.config(state='normal' if company.owned_shares >= 10 else 'disabled')
            company.minus_100_button.config(state='normal' if company.owned_shares >= 100 else 'disabled')
            company.plus_button.config(state='normal' if self.player_cash >= company.current_value else 'disabled')
            company.plus_10_button.config(state='normal' if self.player_cash >= company.current_value * 10 else 'disabled')
            company.plus_100_button.config(state='normal' if self.player_cash >= company.current_value * 100 else 'disabled')

    def refresh_ui(self):
        """Refresh UI elements to reflect current market state"""
        # Get the latest cycle and day numbers from the parent game
        if "stock_market" in self.player_data:
            new_cycle = self.player_data["stock_market"].get("cycle_number", self.cycle_number)
            new_day = self.player_data["stock_market"].get("day_number", self.day_number)
            
            # Check if there's been a cycle change
            cycle_changed = (new_cycle != self.cycle_number) or (new_day != self.day_number)
            
            # Update local values
            self.cycle_number = new_cycle
            self.day_number = new_day
            
            # If the cycle changed, update the timer
            if cycle_changed:
                self.time_left = self.calculate_time_left()
        
        # Update day and cycle label
        current_cycle = (self.cycle_number % 5) + 1  # Ensure displayed cycle is 1-5
        self.day_cycle_label.config(text=f'Day {self.day_number} | Market Cycle {current_cycle}')
        
        # Update company values
        for company in self.companies:
            company.value_label.config(
                text=f"${company.current_value:.2f} (Prev: ${company.previous_value:.2f})"
            )
            
            # Update colors based on change
            if company.current_value > company.previous_value:
                company.value_label.config(foreground="green")
            elif company.current_value < company.previous_value:
                company.value_label.config(foreground="red")
            else:
                company.value_label.config(foreground="black")
        
        # Update button states
        self.update_buttons()
        
        # Schedule next refresh
        self.after_id = self.stock_window.after(5000, self.refresh_ui)  # Refresh every 5 seconds

    def show_price_graph(self, company):
        # Create a new window for the graph
        graph_window = tk.Toplevel(self.stock_window)
        graph_window.title(f"{company.name} Price History")
        graph_window.geometry("400x300")

        # Create the figure and canvas
        fig = Figure(figsize=(4, 3))
        canvas = FigureCanvasTkAgg(fig, master=graph_window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # Create the line plot
        ax = fig.add_subplot(111)
        ax.plot(company.price_history, marker='o')
        ax.set_title(f"{company.name} Price History")
        ax.set_xlabel("Updates")
        ax.set_ylabel("Price ($)")
        ax.grid(True)

        # Rotate x-axis labels for better readability
        plt.xticks(rotation=45)
        fig.tight_layout()

        # Update the canvas
        canvas.draw()

    def on_closing(self):
        # Finalize any pending trades for the current cycle
        self.finalize_cycle_trades()
        
        # Cancel the timer if it exists
        if self.after_id:
            self.stock_window.after_cancel(self.after_id)
        
        # Call the return callback to update parent game with player data
        self.return_callback(self.player_data)
        
        # Destroy the window
        self.stock_window.destroy() 