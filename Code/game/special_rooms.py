import tkinter as tk
from tkinter import ttk, messagebox

class MedBay:
    def __init__(self, parent_window, player_data, return_callback):
        # Create a new toplevel window
        self.medbay_window = tk.Toplevel(parent_window)
        self.medbay_window.title("MedBay")
        self.medbay_window.geometry("800x600")
        self.medbay_window.configure(bg="black")
        
        # Store references
        self.parent_window = parent_window
        self.player_data = player_data
        self.return_callback = return_callback
        
        # Bind window closing
        self.medbay_window.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Ensure this window stays on top
        self.medbay_window.transient(parent_window)
        self.medbay_window.grab_set()
        self.medbay_window.focus_force()
        
        # Center window on screen after window is configured
        self.medbay_window.update_idletasks()
        width = 800
        height = 600
        x = (self.medbay_window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.medbay_window.winfo_screenheight() // 2) - (height // 2)
        self.medbay_window.geometry(f"{width}x{height}+{x}+{y}")
        
        # Title
        room_label = tk.Label(self.medbay_window, text="Station Medical Bay", font=("Arial", 24), bg="black", fg="white")
        room_label.pack(pady=30)
        
        # Description
        desc_label = tk.Label(self.medbay_window, 
                              text="The medical bay is clean and orderly. Various medical equipment lines the walls, and a few examination beds are visible. The station's medical staff handle everything from routine checkups to emergency trauma care.",
                              font=("Arial", 12), bg="black", fg="white", wraplength=600)
        desc_label.pack(pady=10)
        
        # Room actions
        self.button_frame = tk.Frame(self.medbay_window, bg="black")
        self.button_frame.pack(pady=20)
        
        # Check if user has special access
        has_medbay_access = "permissions" in self.player_data and self.player_data["permissions"].get("medbay_station", False)
        
        if has_medbay_access:
            # Show station access button for authorized personnel
            station_btn = tk.Button(self.button_frame, text="Enter MedBay Station", font=("Arial", 14), width=20, command=self.access_medbay_station)
            station_btn.pack(pady=10)
            
            # Add door lock/unlock button for authorized personnel
            door_btn = tk.Button(self.button_frame, text="Lock/Unlock MedBay Door", font=("Arial", 14), width=20, command=self.toggle_door_lock)
            door_btn.pack(pady=10)
            
            # Add "Room Options" button to show regular options
            options_btn = tk.Button(self.button_frame, text="Room Options", font=("Arial", 14), width=20, command=self.show_room_options)
            options_btn.pack(pady=10)
        else:
            # Show regular options for unauthorized personnel
            self.show_room_options()
        
        # Exit button
        exit_btn = tk.Button(self.medbay_window, text="Exit Room", font=("Arial", 14), width=15, command=self.on_closing)
        exit_btn.pack(pady=20)
    
    def show_room_options(self):
        """Show regular room options that all players can access"""
        # Health check option
        health_check_btn = tk.Button(self.button_frame, text="Request Health Check", font=("Arial", 14), width=20, command=self.health_check)
        health_check_btn.pack(pady=10)
    
    def health_check(self):
        # Show dialog with the room window as parent to keep focus within the room
        self.medbay_window.after(10, lambda: messagebox.showinfo("Health Check Results", "Everything is fine.", parent=self.medbay_window))
        # Make sure the window stays on top after dialog
        self.medbay_window.after(20, self.medbay_window.lift)
        self.medbay_window.focus_force()
    
    def access_medbay_station(self):
        # Show access confirmation for authorized personnel
        self.medbay_window.after(10, lambda: messagebox.showinfo("MedBay Station", "Access granted. Welcome to the MedBay Station.", parent=self.medbay_window))
        # Make sure the window stays on top after dialog
        self.medbay_window.after(20, self.medbay_window.lift)
        self.medbay_window.focus_force()
    
    def toggle_door_lock(self):
        # Get the door location key
        door_key = "0,6"
        
        # Get the ship map from player data (need to pass it via player_data)
        if "ship_map" not in self.player_data:
            self.medbay_window.after(10, lambda: messagebox.showinfo("Door Control", "Unable to access door control system.", parent=self.medbay_window))
            return
            
        ship_map = self.player_data["ship_map"]
        if door_key not in ship_map:
            self.medbay_window.after(10, lambda: messagebox.showinfo("Door Control", "Unable to access door control system.", parent=self.medbay_window))
            return
            
        # Toggle the door lock
        if ship_map[door_key].get("locked", False):
            ship_map[door_key]["locked"] = False
            ship_map[door_key]["desc"] = "The medical facility of the station. The door is unlocked."
            self.medbay_window.after(10, lambda: messagebox.showinfo("Door Control", "The MedBay door has been unlocked.", parent=self.medbay_window))
        else:
            ship_map[door_key]["locked"] = True
            ship_map[door_key]["desc"] = "The medical facility of the station. The door is locked."
            self.medbay_window.after(10, lambda: messagebox.showinfo("Door Control", "The MedBay door has been locked.", parent=self.medbay_window))
        
        # Update ship map in player data
        self.player_data["ship_map"] = ship_map
        
        # Make sure the window stays on top after dialog
        self.medbay_window.after(20, self.medbay_window.lift)
        self.medbay_window.focus_force()
    
    def on_closing(self):
        # Release grab before closing
        self.medbay_window.grab_release()
        
        # Call return callback with player data
        self.return_callback(self.player_data)
        
        # Destroy the window
        self.medbay_window.destroy()

class Bridge:
    def __init__(self, parent_window, player_data, return_callback):
        # Create a new toplevel window
        self.bridge_window = tk.Toplevel(parent_window)
        self.bridge_window.title("Bridge")
        self.bridge_window.geometry("800x600")
        self.bridge_window.configure(bg="black")
        
        # Store references
        self.parent_window = parent_window
        self.player_data = player_data
        self.return_callback = return_callback
        
        # Bind window closing
        self.bridge_window.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Ensure this window stays on top
        self.bridge_window.transient(parent_window)
        self.bridge_window.grab_set()
        self.bridge_window.focus_force()
        
        # Center window on screen after window is configured
        self.bridge_window.update_idletasks()
        width = 800
        height = 600
        x = (self.bridge_window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.bridge_window.winfo_screenheight() // 2) - (height // 2)
        self.bridge_window.geometry(f"{width}x{height}+{x}+{y}")
        
        # Title
        room_label = tk.Label(self.bridge_window, text="Station Bridge", font=("Arial", 24), bg="black", fg="white")
        room_label.pack(pady=30)
        
        # Description
        desc_label = tk.Label(self.bridge_window, 
                              text="The bridge is the command center of the station. Multiple workstations with monitors displaying various station systems are arranged around the room. This is where the Captain and Department Heads coordinate station operations.",
                              font=("Arial", 12), bg="black", fg="white", wraplength=600)
        desc_label.pack(pady=10)
        
        # Room actions
        self.button_frame = tk.Frame(self.bridge_window, bg="black")
        self.button_frame.pack(pady=20)
        
        # Check if user has special access
        has_bridge_access = "permissions" in self.player_data and self.player_data["permissions"].get("bridge_station", False)
        
        if has_bridge_access:
            # Show station access button for authorized personnel
            station_btn = tk.Button(self.button_frame, text="Enter Bridge Station", font=("Arial", 14), width=20, command=self.access_bridge_station)
            station_btn.pack(pady=10)
            
            # Add door lock/unlock button for authorized personnel
            door_btn = tk.Button(self.button_frame, text="Lock/Unlock Bridge Door", font=("Arial", 14), width=20, command=self.toggle_door_lock)
            door_btn.pack(pady=10)
            
            # Add "Room Options" button to show regular options
            options_btn = tk.Button(self.button_frame, text="Room Options", font=("Arial", 14), width=20, command=self.show_room_options)
            options_btn.pack(pady=10)
        else:
            # Show regular options for unauthorized personnel
            self.show_room_options()
        
        # Exit button
        exit_btn = tk.Button(self.bridge_window, text="Exit Room", font=("Arial", 14), width=15, command=self.on_closing)
        exit_btn.pack(pady=20)
    
    def show_room_options(self):
        """Show regular room options that all players can access"""
        # Talk to leadership option
        talk_btn = tk.Button(self.button_frame, text="Talk to Ship Leadership", font=("Arial", 14), width=20, command=self.talk_to_leadership)
        talk_btn.pack(pady=10)
    
    def talk_to_leadership(self):
        # Show dialog with the room window as parent to keep focus within the room
        self.bridge_window.after(10, lambda: messagebox.showinfo("Bridge", "Captain and Department Heads are not in.", parent=self.bridge_window))
        # Make sure the window stays on top after dialog
        self.bridge_window.after(20, self.bridge_window.lift)
        self.bridge_window.focus_force()
    
    def access_bridge_station(self):
        # Show access confirmation for authorized personnel
        self.bridge_window.after(10, lambda: messagebox.showinfo("Bridge Station", "Access granted. Welcome to the Bridge Station.", parent=self.bridge_window))
        # Make sure the window stays on top after dialog
        self.bridge_window.after(20, self.bridge_window.lift)
        self.bridge_window.focus_force()
    
    def toggle_door_lock(self):
        # Get the door location key
        door_key = "6,0"
        
        # Get the ship map from player data
        if "ship_map" not in self.player_data:
            self.bridge_window.after(10, lambda: messagebox.showinfo("Door Control", "Unable to access door control system.", parent=self.bridge_window))
            return
            
        ship_map = self.player_data["ship_map"]
        if door_key not in ship_map:
            self.bridge_window.after(10, lambda: messagebox.showinfo("Door Control", "Unable to access door control system.", parent=self.bridge_window))
            return
            
        # Toggle the door lock
        if ship_map[door_key].get("locked", False):
            ship_map[door_key]["locked"] = False
            ship_map[door_key]["desc"] = "The control center of the station. The door is unlocked."
            self.bridge_window.after(10, lambda: messagebox.showinfo("Door Control", "The Bridge door has been unlocked.", parent=self.bridge_window))
        else:
            ship_map[door_key]["locked"] = True
            ship_map[door_key]["desc"] = "The control center of the station. The door is locked."
            self.bridge_window.after(10, lambda: messagebox.showinfo("Door Control", "The Bridge door has been locked.", parent=self.bridge_window))
        
        # Update ship map in player data
        self.player_data["ship_map"] = ship_map
        
        # Make sure the window stays on top after dialog
        self.bridge_window.after(20, self.bridge_window.lift)
        self.bridge_window.focus_force()
    
    def on_closing(self):
        # Release grab before closing
        self.bridge_window.grab_release()
        
        # Call return callback with player data
        self.return_callback(self.player_data)
        
        # Destroy the window
        self.bridge_window.destroy()

class Security:
    def __init__(self, parent_window, player_data, return_callback):
        # Create a new toplevel window
        self.security_window = tk.Toplevel(parent_window)
        self.security_window.title("Security")
        self.security_window.geometry("800x600")
        self.security_window.configure(bg="black")
        
        # Store references
        self.parent_window = parent_window
        self.player_data = player_data
        self.return_callback = return_callback
        
        # Bind window closing
        self.security_window.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Ensure this window stays on top
        self.security_window.transient(parent_window)
        self.security_window.grab_set()
        self.security_window.focus_force()
        
        # Center window on screen after window is configured
        self.security_window.update_idletasks()
        width = 800
        height = 600
        x = (self.security_window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.security_window.winfo_screenheight() // 2) - (height // 2)
        self.security_window.geometry(f"{width}x{height}+{x}+{y}")
        
        # Title
        room_label = tk.Label(self.security_window, text="Station Security Office", font=("Arial", 24), bg="black", fg="white")
        room_label.pack(pady=30)
        
        # Description
        desc_label = tk.Label(self.security_window, 
                              text="The security office is filled with monitoring equipment. Screens showing various parts of the station line the walls. A few security officers monitor the feeds, while weapon lockers are secured along one wall.",
                              font=("Arial", 12), bg="black", fg="white", wraplength=600)
        desc_label.pack(pady=10)
        
        # Room actions
        self.button_frame = tk.Frame(self.security_window, bg="black")
        self.button_frame.pack(pady=20)
        
        # Check if user has special access
        has_security_access = "permissions" in self.player_data and self.player_data["permissions"].get("security_station", False)
        
        if has_security_access:
            # Show station access button for authorized personnel
            station_btn = tk.Button(self.button_frame, text="Enter Security Station", font=("Arial", 14), width=20, command=self.access_security_station)
            station_btn.pack(pady=10)
            
            # Add door lock/unlock button for authorized personnel
            door_btn = tk.Button(self.button_frame, text="Lock/Unlock Security Door", font=("Arial", 14), width=20, command=self.toggle_door_lock)
            door_btn.pack(pady=10)
            
            # Add "Room Options" button to show regular options
            options_btn = tk.Button(self.button_frame, text="Room Options", font=("Arial", 14), width=20, command=self.show_room_options)
            options_btn.pack(pady=10)
        else:
            # Show regular options for unauthorized personnel
            self.show_room_options()
        
        # Exit button
        exit_btn = tk.Button(self.security_window, text="Exit Room", font=("Arial", 14), width=15, command=self.on_closing)
        exit_btn.pack(pady=20)
    
    def show_room_options(self):
        """Show regular room options that all players can access"""
        # Talk to guard option
        guard_btn = tk.Button(self.button_frame, text="Talk to Security Guard", font=("Arial", 14), width=20, command=self.talk_to_guard)
        guard_btn.pack(pady=10)
    
    def talk_to_guard(self):
        # Show dialog with the room window as parent to keep focus within the room
        self.security_window.after(10, lambda: messagebox.showinfo("Security Guard", "The security agent waves you away without looking up from the cameras.", parent=self.security_window))
        # Make sure the window stays on top after dialog
        self.security_window.after(20, self.security_window.lift)
        self.security_window.focus_force()
    
    def access_security_station(self):
        # Show access confirmation for authorized personnel
        self.security_window.after(10, lambda: messagebox.showinfo("Security Station", "Access granted. Welcome to the Security Station.", parent=self.security_window))
        # Make sure the window stays on top after dialog
        self.security_window.after(20, self.security_window.lift)
        self.security_window.focus_force()
    
    def toggle_door_lock(self):
        # Get the door location key
        door_key = "6,6"
        
        # Get the ship map from player data
        if "ship_map" not in self.player_data:
            self.security_window.after(10, lambda: messagebox.showinfo("Door Control", "Unable to access door control system.", parent=self.security_window))
            return
            
        ship_map = self.player_data["ship_map"]
        if door_key not in ship_map:
            self.security_window.after(10, lambda: messagebox.showinfo("Door Control", "Unable to access door control system.", parent=self.security_window))
            return
            
        # Toggle the door lock
        if ship_map[door_key].get("locked", False):
            ship_map[door_key]["locked"] = False
            ship_map[door_key]["desc"] = "The security center of the station. The door is unlocked."
            self.security_window.after(10, lambda: messagebox.showinfo("Door Control", "The Security door has been unlocked.", parent=self.security_window))
        else:
            ship_map[door_key]["locked"] = True
            ship_map[door_key]["desc"] = "The security center of the station. The door is locked."
            self.security_window.after(10, lambda: messagebox.showinfo("Door Control", "The Security door has been locked.", parent=self.security_window))
        
        # Update ship map in player data
        self.player_data["ship_map"] = ship_map
        
        # Make sure the window stays on top after dialog
        self.security_window.after(20, self.security_window.lift)
        self.security_window.focus_force()
    
    def on_closing(self):
        # Release grab before closing
        self.security_window.grab_release()
        
        # Call return callback with player data
        self.return_callback(self.player_data)
        
        # Destroy the window
        self.security_window.destroy() 