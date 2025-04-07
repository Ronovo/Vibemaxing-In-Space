import tkinter as tk
import random
import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import messagebox, ttk

class Company:
    def __init__(self, name, starting_value):
        self.name = name
        self.current_value = starting_value
        self.previous_value = starting_value
        self.price_history = [starting_value]
        self.owned_shares = 0
        
    def update_value(self):
        """Update the company's stock value"""
        # Store the previous value for reference
        self.previous_value = self.current_value
        
        # Random change between -10% and +10%
        change = random.uniform(-0.10, 0.10)
        
        # Apply change
        self.current_value = max(1.0, self.current_value * (1 + change))
        
        # Add to price history
        self.price_history.append(self.current_value)
        
        # Limit price history to most recent 50 cycles
        if len(self.price_history) > 50:
            self.price_history.pop(0)

class StockMarket:
    def __init__(self, parent_window, player_data, companies, cycle_number, day_number, return_callback):
        # Create a new toplevel window
        self.stock_window = tk.Toplevel(parent_window)
        self.stock_window.title("Stock Market")
        self.stock_window.geometry("1000x600")
        self.stock_window.configure(bg="black")
        
        # Store references
        self.parent_window = parent_window
        self.player_data = player_data
        self.companies = companies
        self.cycle_number = cycle_number
        self.day_number = day_number
        self.return_callback = return_callback
        self.current_company = None
        
        # Track transactions for notes
        self.stock_transactions = []
        
        # Bind window closing
        self.stock_window.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Ensure this window stays on top
        self.stock_window.transient(parent_window)
        self.stock_window.grab_set()
        
        # Load company owned shares from player data
        if "stock_holdings" in player_data:
            for company in self.companies:
                company.owned_shares = player_data["stock_holdings"].get(company.name, 0)
        
        # Create main frames
        self.left_frame = tk.Frame(self.stock_window, bg="black", width=300)
        self.left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
        
        self.right_frame = tk.Frame(self.stock_window, bg="black")
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Info labels
        self.info_frame = tk.Frame(self.left_frame, bg="black")
        self.info_frame.pack(fill=tk.X, pady=10)
        
        self.cycle_label = tk.Label(self.info_frame, text=f"Cycle: {self.cycle_number}", 
                                   font=("Arial", 12), bg="black", fg="white")
        self.cycle_label.grid(row=0, column=0, sticky="w", pady=2)
        
        self.day_label = tk.Label(self.info_frame, text=f"Day: {self.day_number}", 
                                 font=("Arial", 12), bg="black", fg="white")
        self.day_label.grid(row=1, column=0, sticky="w", pady=2)
        
        self.credits_label = tk.Label(self.info_frame, text=f"Credits: {player_data['credits']:.2f}", 
                                    font=("Arial", 12), bg="black", fg="white")
        self.credits_label.grid(row=2, column=0, sticky="w", pady=2)
        
        # Companies list
        self.companies_listbox = tk.Listbox(self.left_frame, 
                                         font=("Arial", 12), bg="black", fg="white",
                                         selectbackground="#333333", selectforeground="white",
                                         width=30, height=15)
        self.companies_listbox.pack(pady=10, fill=tk.BOTH, expand=True)
        
        # Fill the companies listbox
        for company in self.companies:
            self.companies_listbox.insert(tk.END, company.name)
        
        # Bind selection event
        self.companies_listbox.bind('<<ListboxSelect>>', self.on_company_select)
        
        # Add Trade History button
        self.history_btn = tk.Button(self.left_frame, text="View Trade History", 
                                   font=("Arial", 12), bg="#333333", fg="white",
                                   command=self.show_trade_history)
        self.history_btn.pack(pady=10, fill=tk.X)
        
        # Back button
        self.back_btn = tk.Button(self.left_frame, text="Back to Computer", 
                                font=("Arial", 12), bg="#333333", fg="white",
                                command=self.on_closing)
        self.back_btn.pack(pady=10, fill=tk.X)
        
        # Right frame contents (will be populated when company is selected)
        self.company_info_frame = tk.Frame(self.right_frame, bg="black")
        self.company_info_frame.pack(fill=tk.X, pady=10)
        
        # Set up the figure for the graph
        self.fig = plt.Figure(figsize=(5, 3), dpi=100)
        self.fig.patch.set_facecolor('black')
        self.ax = self.fig.add_subplot(111)
        self.ax.set_facecolor('black')
        self.ax.tick_params(colors='white')
        self.ax.spines['bottom'].set_color('white')
        self.ax.spines['top'].set_color('white')
        self.ax.spines['left'].set_color('white')
        self.ax.spines['right'].set_color('white')
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.right_frame)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.configure(bg="black", highlightbackground="black")
        self.canvas_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Trade buttons frame
        self.trade_frame = tk.Frame(self.right_frame, bg="black")
        self.trade_frame.pack(fill=tk.X, pady=10)
        
        # Select first company by default
        if self.companies_listbox.size() > 0:
            self.companies_listbox.selection_set(0)
            self.on_company_select(None)  # Trigger the selection handler
    
    def on_company_select(self, event):
        """Handle company selection from the listbox"""
        if not self.companies_listbox.curselection():
            return
            
        selection = self.companies_listbox.curselection()[0]
        self.current_company = self.companies[selection]
        
        # Clear company info frame
        for widget in self.company_info_frame.winfo_children():
            widget.destroy()
            
        # Clear trade frame
        for widget in self.trade_frame.winfo_children():
            widget.destroy()
        
        # Add company information
        company_name = tk.Label(self.company_info_frame, text=self.current_company.name, 
                              font=("Arial", 18, "bold"), bg="black", fg="white")
        company_name.grid(row=0, column=0, columnspan=2, sticky="w", pady=5)
        
        current_price = tk.Label(self.company_info_frame, text=f"Current Price: {self.current_company.current_value:.2f}", 
                               font=("Arial", 12), bg="black", fg="white")
        current_price.grid(row=1, column=0, sticky="w", pady=2)
        
        # Calculate price change
        price_change = self.current_company.current_value - self.current_company.previous_value
        price_change_pct = (price_change / self.current_company.previous_value) * 100
        
        # Choose color based on price change
        change_color = "green" if price_change >= 0 else "red"
        
        price_change_label = tk.Label(self.company_info_frame, 
                                    text=f"Change: {price_change:.2f} ({price_change_pct:.2f}%)", 
                                    font=("Arial", 12), bg="black", fg=change_color)
        price_change_label.grid(row=1, column=1, sticky="w", pady=2)
        
        shares_owned = tk.Label(self.company_info_frame, 
                              text=f"Shares Owned: {self.current_company.owned_shares}", 
                              font=("Arial", 12), bg="black", fg="white")
        shares_owned.grid(row=2, column=0, sticky="w", pady=2)
        
        # Calculate total value of owned shares
        total_value = self.current_company.owned_shares * self.current_company.current_value
        
        shares_value = tk.Label(self.company_info_frame, 
                              text=f"Total Value: {total_value:.2f}", 
                              font=("Arial", 12), bg="black", fg="white")
        shares_value.grid(row=2, column=1, sticky="w", pady=2)
        
        # Update the graph
        self.update_graph()
        
        # Add trade interface
        self.create_trade_interface()
    
    def update_graph(self):
        """Update the price history graph for the selected company"""
        if not self.current_company:
            return
            
        # Clear the axis
        self.ax.clear()
        
        # Set up the plot
        self.ax.set_facecolor('black')
        self.ax.tick_params(colors='white')
        
        # Plot the price history
        prices = self.current_company.price_history
        x = range(len(prices))
        
        # Determine plot color based on price trend
        if prices[-1] >= prices[0]:
            line_color = 'green'
        else:
            line_color = 'red'
            
        self.ax.plot(x, prices, color=line_color)
        
        # Set labels
        self.ax.set_title(f"{self.current_company.name} Price History", color='white')
        self.ax.set_xlabel("Cycles", color='white')
        self.ax.set_ylabel("Price", color='white')
        
        # Remove grid
        self.ax.grid(False)
        
        # Draw the canvas
        self.canvas.draw()
    
    def create_trade_interface(self):
        """Create the interface for buying and selling stocks"""
        # Shares to trade label and entry
        shares_label = tk.Label(self.trade_frame, text="Shares:", 
                              font=("Arial", 12), bg="black", fg="white")
        shares_label.grid(row=0, column=0, padx=5, pady=10)
        
        # Dropdown for predefined amounts
        share_options = [1, 5, 10, 25, 50, 100]
        self.shares_var = tk.StringVar(value="1")
        
        shares_dropdown = ttk.Combobox(self.trade_frame, textvariable=self.shares_var, 
                                     values=share_options, width=5)
        shares_dropdown.grid(row=0, column=1, padx=5, pady=10)
        
        # Make the dropdown user editable
        shares_dropdown.config(state="normal")
        
        # Calculate max shares that can be bought
        max_can_buy = int(self.player_data["credits"] / self.current_company.current_value)
        
        # Add max button
        max_buy_btn = tk.Button(self.trade_frame, text=f"Max ({max_can_buy})", 
                              font=("Arial", 10), bg="#333333", fg="white",
                              command=lambda: self.shares_var.set(str(max_can_buy)))
        max_buy_btn.grid(row=0, column=2, padx=5, pady=10)
        
        # Calculate total cost
        def update_total_cost(*args):
            try:
                shares = int(self.shares_var.get())
                total = shares * self.current_company.current_value
                total_label.config(text=f"Total: {total:.2f}")
                
                # Update buy button state
                if shares > 0 and total <= self.player_data["credits"]:
                    buy_btn.config(state=tk.NORMAL)
                else:
                    buy_btn.config(state=tk.DISABLED)
                    
                # Update sell button state
                if shares > 0 and shares <= self.current_company.owned_shares:
                    sell_btn.config(state=tk.NORMAL)
                else:
                    sell_btn.config(state=tk.DISABLED)
                    
            except ValueError:
                total_label.config(text="Total: 0.00")
                buy_btn.config(state=tk.DISABLED)
                sell_btn.config(state=tk.DISABLED)
        
        # Register callback for share amount changes
        self.shares_var.trace("w", update_total_cost)
        
        # Total cost label
        total_label = tk.Label(self.trade_frame, text="Total: 0.00", 
                            font=("Arial", 12), bg="black", fg="white")
        total_label.grid(row=0, column=3, padx=20, pady=10)
        
        # Buy button
        buy_btn = tk.Button(self.trade_frame, text="Buy", font=("Arial", 12), 
                         bg="green", fg="white", width=8,
                         command=self.buy_stock)
        buy_btn.grid(row=1, column=0, padx=10, pady=10)
        
        # Sell button
        sell_btn = tk.Button(self.trade_frame, text="Sell", font=("Arial", 12), 
                          bg="red", fg="white", width=8,
                          command=self.sell_stock)
        sell_btn.grid(row=1, column=1, padx=10, pady=10)
        
        # Initialize button states
        update_total_cost()
    
    def buy_stock(self):
        """Buy stock of the currently selected company"""
        try:
            # Get share amount
            shares = int(self.shares_var.get())
            
            # Calculate total cost
            total_cost = shares * self.current_company.current_value
            
            # Check if player has enough credits
            if total_cost > self.player_data["credits"]:
                messagebox.showerror("Transaction Failed", "Not enough credits for this purchase.")
                return
                
            # Update player credits
            self.player_data["credits"] -= total_cost
            
            # Update company owned shares
            self.current_company.owned_shares += shares
            
            # Update stock holdings in player data
            if "stock_holdings" not in self.player_data:
                self.player_data["stock_holdings"] = {}
                
            if self.current_company.name not in self.player_data["stock_holdings"]:
                self.player_data["stock_holdings"][self.current_company.name] = shares
            else:
                self.player_data["stock_holdings"][self.current_company.name] += shares
            
            # Track transaction for notes
            transaction = {
                "type": "buy",
                "company": self.current_company.name,
                "shares": shares,
                "price": self.current_company.current_value,
                "total": total_cost,
                "timestamp": datetime.datetime.now().isoformat()
            }
            self.stock_transactions.append(transaction)
            
            # Update display
            self.credits_label.config(text=f"Credits: {self.player_data['credits']:.2f}")
            
            # Recalculate max shares
            max_can_buy = int(self.player_data["credits"] / self.current_company.current_value)
            
            # Show success message
            messagebox.showinfo("Transaction Complete", 
                               f"Bought {shares} shares of {self.current_company.name} for {total_cost:.2f} credits.")
            
            # Refresh company info
            self.on_company_select(None)
        except ValueError:
            messagebox.showerror("Input Error", "Please enter a valid number of shares.")
    
    def sell_stock(self):
        """Sell stock of the currently selected company"""
        try:
            # Get share amount
            shares = int(self.shares_var.get())
            
            # Check if player owns enough shares
            if shares > self.current_company.owned_shares:
                messagebox.showerror("Transaction Failed", "You don't own that many shares.")
                return
                
            # Calculate total value
            total_value = shares * self.current_company.current_value
            
            # Update player credits
            self.player_data["credits"] += total_value
            
            # Update company owned shares
            self.current_company.owned_shares -= shares
            
            # Update stock holdings in player data
            if "stock_holdings" in self.player_data and self.current_company.name in self.player_data["stock_holdings"]:
                self.player_data["stock_holdings"][self.current_company.name] -= shares
                
                # Remove entry if no shares left
                if self.player_data["stock_holdings"][self.current_company.name] <= 0:
                    del self.player_data["stock_holdings"][self.current_company.name]
            
            # Calculate profit/loss if we have the purchase price history
            profit = 0
            if "stock_purchases" in self.player_data and self.current_company.name in self.player_data["stock_purchases"]:
                # Get the average purchase price of shares
                purchases = self.player_data["stock_purchases"][self.current_company.name]
                if len(purchases) > 0:
                    # Calculate average purchase price of shares being sold
                    total_cost = sum(purchase["price"] * purchase["shares"] for purchase in purchases[:shares])
                    avg_price = total_cost / shares if shares > 0 else 0
                    
                    # Calculate profit/loss
                    profit = total_value - (avg_price * shares)
            
            # Track transaction for notes
            transaction = {
                "type": "sell",
                "company": self.current_company.name,
                "shares": shares,
                "price": self.current_company.current_value,
                "total": total_value,
                "profit": profit,
                "timestamp": datetime.datetime.now().isoformat()
            }
            self.stock_transactions.append(transaction)
            
            # Update display
            self.credits_label.config(text=f"Credits: {self.player_data['credits']:.2f}")
            
            # Success message
            profit_text = ""
            if profit != 0:
                if profit > 0:
                    profit_text = f" (Profit: {profit:.2f} credits)"
                else:
                    profit_text = f" (Loss: {abs(profit):.2f} credits)"
                    
            messagebox.showinfo("Transaction Complete", 
                               f"Sold {shares} shares of {self.current_company.name} for {total_value:.2f} credits.{profit_text}")
            
            # Refresh company info
            self.on_company_select(None)
        except ValueError:
            messagebox.showerror("Input Error", "Please enter a valid number of shares.")
    
    def show_trade_history(self):
        """Show the trade history log"""
        # Create a new toplevel window
        history_window = tk.Toplevel(self.stock_window)
        history_window.title("Trade History")
        history_window.geometry("600x400")
        history_window.configure(bg="black")
        
        # Ensure this window stays on top
        history_window.transient(self.stock_window)
        history_window.grab_set()
        
        # Title
        title_label = tk.Label(history_window, text="Trade History", 
                             font=("Arial", 18), bg="black", fg="white")
        title_label.pack(pady=10)
        
        # Create frame with scrollbar
        frame = tk.Frame(history_window, bg="black")
        frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Add a scrollbar
        scrollbar = tk.Scrollbar(frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Create the trade log text widget
        trade_log = tk.Text(frame, font=("Arial", 12), 
                          bg="black", fg="white", width=60, height=15,
                          yscrollcommand=scrollbar.set)
        trade_log.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=trade_log.yview)
        
        # Populate the trade log
        if "stock_market" in self.player_data and "trade_log" in self.player_data["stock_market"]:
            trade_log.insert(tk.END, "TRADE HISTORY:\n\n")
            
            # Display trade log entries in reverse order (newest first)
            for entry in reversed(self.player_data["stock_market"]["trade_log"]):
                cycle = entry.get("cycle", 0)
                day = entry.get("day", 0)
                trade_log.insert(tk.END, f"Cycle {cycle} (Day {day}):\n")
                
                trades = entry.get("trades", {})
                
                # Bought trades
                if "bought" in trades and trades["bought"]:
                    trade_log.insert(tk.END, "  BOUGHT:\n")
                    for company, data in trades["bought"].items():
                        amount = data.get("amount", 0)
                        price = data.get("price", 0)
                        total = data.get("total", 0)
                        trade_log.insert(tk.END, f"    {company}: {amount} shares @ {price:.2f} cr each = {total:.2f} cr\n")
                
                # Sold trades
                if "sold" in trades and trades["sold"]:
                    trade_log.insert(tk.END, "  SOLD:\n")
                    for company, data in trades["sold"].items():
                        amount = data.get("amount", 0)
                        price = data.get("price", 0)
                        total = data.get("total", 0)
                        trade_log.insert(tk.END, f"    {company}: {amount} shares @ {price:.2f} cr each = {total:.2f} cr\n")
                
                trade_log.insert(tk.END, "\n")
        else:
            trade_log.insert(tk.END, "No trade history available.")
        
        # Make the text widget read-only
        trade_log.config(state=tk.DISABLED)
        
        # Close button
        close_btn = tk.Button(history_window, text="Close", 
                            font=("Arial", 12), bg="#333333", fg="white",
                            command=history_window.destroy)
        close_btn.pack(pady=10)
    
    def on_closing(self):
        """Handle window closing"""
        # Add the stock transactions to the player data to be logged as notes
        if self.stock_transactions:
            self.player_data["stock_transactions"] = self.stock_transactions
        
        # Release the grab and return control to the parent window
        self.stock_window.grab_release()
        
        # Return player data to the main game
        if self.return_callback:
            self.return_callback(self.player_data)
            
        # Destroy the window
        self.stock_window.destroy()
