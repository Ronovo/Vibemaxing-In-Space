import tkinter as tk
from tkinter import ttk, messagebox
import datetime

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
            door_btn = tk.Button(self.button_frame, text="Lock/Unlock Door", font=("Arial", 14), width=20, command=self.toggle_door_lock)
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
        # Clear existing buttons
        for widget in self.button_frame.winfo_children():
            widget.destroy()
            
        # Health check option
        health_check_btn = tk.Button(self.button_frame, text="Request Health Check", font=("Arial", 14), width=20, command=self.health_check)
        health_check_btn.pack(pady=10)
        
        # Talk to doctor option
        talk_doctor_btn = tk.Button(self.button_frame, text="Talk to Doctor", font=("Arial", 14), width=20, command=self.talk_to_doctor)
        talk_doctor_btn.pack(pady=10)
        
        # Only show "Back to Station Menu" if player has access
        has_medbay_access = "permissions" in self.player_data and self.player_data["permissions"].get("medbay_station", False)
        if has_medbay_access:
            # Back to station menu button
            back_btn = tk.Button(self.button_frame, text="Back to Station Menu", font=("Arial", 14), width=20, 
                               command=self.show_station_menu)
            back_btn.pack(pady=10)
    
    def health_check(self):
        # Get the player's limb health data
        limbs = self.player_data.get("limbs", {})
        
        # Create health report
        health_report = "Health Check Results:\n\n"
        
        if not limbs:
            health_report += "No limb health data available."
        else:
            # Calculate overall health percentage
            total_health = sum(limbs.values())
            max_health = len(limbs) * 100
            overall_health = (total_health / max_health) * 100
            
            health_report += f"Overall Health: {overall_health:.1f}%\n\n"
            health_report += "Limb Status:\n"
            
            # Track issues for detailed notes
            injured_limbs = []
            critical_limbs = []
            
            # Add limb statuses
            for limb, health in limbs.items():
                limb_name = limb.replace('_', ' ').title()
                if health > 75:
                    status = "Healthy"
                elif health > 40:
                    status = "Injured"
                    injured_limbs.append(limb_name)
                else:
                    status = "Critical"
                    critical_limbs.append(limb_name)
                health_report += f"- {limb_name}: {health}% ({status})\n"
            
            health_report += "\nRecommendation: "
            if overall_health < 60:
                health_report += "Medical attention recommended."
            else:
                health_report += "No immediate medical attention required."
            
            # Add detailed notes if health is below 100%
            if overall_health < 100:
                health_report += "\n\nDetailed Notes:"
                
                if critical_limbs:
                    health_report += f"\n• Critical damage detected in {', '.join(critical_limbs)}. "
                    health_report += "Immediate treatment required."
                
                if injured_limbs:
                    health_report += f"\n• Moderate trauma detected in {', '.join(injured_limbs)}. "
                    health_report += "Rest and treatment advised."
                
                if overall_health < 75:
                    health_report += "\n• Movement and performance significantly impaired."
                elif overall_health < 90:
                    health_report += "\n• Some physical activities may be difficult."
                
                # Treatment options
                health_report += "\n\nTreatment Options:"
                health_report += "\n• Self-healing through rest"
                health_report += "\n• Medical treatment by qualified doctor (50 credits)"
                if "permissions" in self.player_data and self.player_data["permissions"].get("medbay_station", False):
                    health_report += "\n• Advanced treatment available at MedBay Station"
        
        # Show dialog with the room window as parent to keep focus within the room
        self.medbay_window.after(10, lambda: messagebox.showinfo("Medical Scan", health_report, parent=self.medbay_window))
        # Make sure the window stays on top after dialog
        self.medbay_window.after(20, self.medbay_window.lift)
        self.medbay_window.focus_force()
    
    def talk_to_doctor(self):
        """Talk to a doctor who can provide healing for a fee"""
        # Check if player has any injuries
        is_injured = False
        for limb, health in self.player_data.get("limbs", {}).items():
            if health < 100:
                is_injured = True
                break
        
        if not is_injured:
            # No injuries to heal
            message = "The doctor examines you. 'You're in perfect health! No treatment needed.'"
            self.medbay_window.after(10, lambda: messagebox.showinfo("Doctor", message, parent=self.medbay_window))
        else:
            # Player has injuries, offer healing for credits
            message = "The doctor examines you. 'I can treat all your injuries for 50 credits. Would you like to proceed?'"
            
            # Create a custom dialog with Yes/No buttons
            dialog = tk.Toplevel(self.medbay_window)
            dialog.title("Doctor")
            dialog.geometry("400x150")
            dialog.configure(bg="black")
            dialog.transient(self.medbay_window)
            dialog.grab_set()
            
            # Center the dialog relative to the parent window
            dialog.geometry(f"+{self.medbay_window.winfo_rootx() + 200}+{self.medbay_window.winfo_rooty() + 200}")
            
            # Message
            tk.Label(dialog, text=message, font=("Arial", 12), bg="black", fg="white", wraplength=350).pack(pady=10)
            
            # Buttons frame
            btn_frame = tk.Frame(dialog, bg="black")
            btn_frame.pack(pady=10)
            
            # Yes button
            yes_btn = tk.Button(btn_frame, text="Yes (50 credits)", font=("Arial", 12), 
                             command=lambda: self.pay_for_healing(dialog))
            yes_btn.pack(side=tk.LEFT, padx=10)
            
            # No button
            no_btn = tk.Button(btn_frame, text="No", font=("Arial", 12), 
                             command=dialog.destroy)
            no_btn.pack(side=tk.LEFT, padx=10)
    
    def pay_for_healing(self, dialog):
        """Pay credits for healing"""
        # Check if player has enough credits
        if self.player_data["credits"] < 50:
            message = "You don't have enough credits for treatment. Come back when you can afford it."
            dialog.destroy()
            self.medbay_window.after(10, lambda: messagebox.showinfo("Doctor", message, parent=self.medbay_window))
            return
        
        # Deduct credits
        self.player_data["credits"] -= 50
        
        # Store original health values for report
        original_health = self.player_data["limbs"].copy()
        
        # Heal all limbs to 100%
        for limb in self.player_data["limbs"]:
            self.player_data["limbs"][limb] = 100
        
        # Close the dialog
        dialog.destroy()
        
        # Create healing report
        healing_report = "You paid 50 credits for medical treatment.\n\n"
        healing_report += "All injuries have been treated.\n\n"
        healing_report += "Previously injured areas:\n"
        
        # Track injured limbs for note
        has_injuries = False
        injured_limbs = []
        
        # Show previous health values for injured limbs
        for limb, health in original_health.items():
            if health < 100:
                has_injuries = True
                limb_name = limb.replace('_', ' ').title()
                healing_report += f"- {limb_name}: {health}% → 100%\n"
                injured_limbs.append(f"{limb_name} ({health}% → 100%)")
        
        if not has_injuries:
            healing_report += "None - you were already in perfect health.\n"
            healing_report += "The doctor still charges you for the examination."
            
        # Show healing results
        self.medbay_window.after(10, lambda: messagebox.showinfo("Medical Treatment", healing_report, parent=self.medbay_window))
        
        # Add note about the treatment
        if "notes" in self.player_data:
            if has_injuries:
                note_text = f"Paid 50 credits for medical treatment. Healed: {', '.join(injured_limbs)}"
            else:
                note_text = "Paid 50 credits for medical examination. No injuries were found."
                
            # Add note using timestamp
            self.player_data["notes"].append({
                "timestamp": datetime.datetime.now().isoformat(),
                "text": note_text
            })
        
        # Make sure the window stays on top after dialog
        self.medbay_window.after(20, self.medbay_window.lift)
        self.medbay_window.focus_force()
    
    def access_medbay_station(self):
        # Show medbay station options for authorized personnel
        # Clear existing buttons
        for widget in self.button_frame.winfo_children():
            widget.destroy()
            
        # Add healing option
        heal_btn = tk.Button(self.button_frame, text="Heal Injuries", font=("Arial", 14), width=20, command=self.heal_player)
        heal_btn.pack(pady=10)
        
        # Back button
        back_btn = tk.Button(self.button_frame, text="Back to Station Menu", font=("Arial", 14), width=20, 
                           command=self.show_station_menu)
        back_btn.pack(pady=10)
    
    def heal_player(self):
        """Heal the player's limbs to full health"""
        # Check if player has limb data
        if "limbs" in self.player_data:
            # Store original health values for report
            original_health = self.player_data["limbs"].copy()
            
            # Heal all limbs to 100%
            for limb in self.player_data["limbs"]:
                self.player_data["limbs"][limb] = 100
            
            # Create healing report
            healing_report = "Medical Treatment Results:\n\n"
            healing_report += "All limbs restored to full health.\n\n"
            healing_report += "Previous Status:\n"
            
            # Check if there were any injuries to track
            had_injuries = False
            injury_details = []
            
            # Show previous health values
            for limb, health in original_health.items():
                limb_name = limb.replace('_', ' ').title()
                healing_report += f"- {limb_name}: {health}% → 100%\n"
                
                # Track injuries for note
                if health < 100:
                    had_injuries = True
                    injury_details.append(f"{limb_name} ({health}% → 100%)")
            
            # Show dialog with healing results
            self.medbay_window.after(10, lambda: messagebox.showinfo("Medical Treatment", healing_report, parent=self.medbay_window))
            
            # Add note about healing if there were injuries
            if had_injuries and "notes" in self.player_data:
                note_text = f"Received advanced medical treatment at MedBay Station. Healed: {', '.join(injury_details)}"
                
                # Add note
                self.player_data["notes"].append({
                    "timestamp": datetime.datetime.now().isoformat(),
                    "text": note_text
                })
                
        else:
            self.medbay_window.after(10, lambda: messagebox.showinfo("Medical Treatment", "No injuries to treat.", parent=self.medbay_window))
        
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
        # Check if the door is locked
        door_key = "0,6"  # MedBay door
        if self.player_data.get("ship_map", {}).get(door_key, {}).get("locked", False):
            self.medbay_window.after(10, lambda: messagebox.showinfo("Locked Door", "The door is locked. You must unlock it before leaving.", parent=self.medbay_window))
            # Make sure the window stays on top after dialog
            self.medbay_window.after(20, self.medbay_window.lift)
            self.medbay_window.focus_force()
            return
        
        # Release grab before closing
        self.medbay_window.grab_release()
        
        # Call return callback with player data
        self.return_callback(self.player_data)
        
        # Destroy the window
        self.medbay_window.destroy()

    def show_station_menu(self):
        """Return to main station menu options"""
        # Clear existing buttons
        for widget in self.button_frame.winfo_children():
            widget.destroy()
            
        # Check if user has special access
        has_medbay_access = "permissions" in self.player_data and self.player_data["permissions"].get("medbay_station", False)
        
        if has_medbay_access:
            # Show station access button for authorized personnel
            station_btn = tk.Button(self.button_frame, text="Enter MedBay Station", font=("Arial", 14), width=20, command=self.access_medbay_station)
            station_btn.pack(pady=10)
            
            # Add door lock/unlock button for authorized personnel
            door_btn = tk.Button(self.button_frame, text="Lock/Unlock Door", font=("Arial", 14), width=20, command=self.toggle_door_lock)
            door_btn.pack(pady=10)
            
            # Add "Room Options" button to show regular options
            options_btn = tk.Button(self.button_frame, text="Room Options", font=("Arial", 14), width=20, command=self.show_room_options)
            options_btn.pack(pady=10)
        else:
            # Show regular options for unauthorized personnel
            self.show_room_options()

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
            door_btn = tk.Button(self.button_frame, text="Lock/Unlock Door", font=("Arial", 14), width=20, command=self.toggle_door_lock)
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
        # Clear existing buttons
        for widget in self.button_frame.winfo_children():
            widget.destroy()
            
        # Talk to leadership option
        talk_btn = tk.Button(self.button_frame, text="Talk to Ship Leadership", font=("Arial", 14), width=20, command=self.talk_to_leadership)
        talk_btn.pack(pady=10)
        
        # Only show "Back to Station Menu" if player has access
        has_bridge_access = "permissions" in self.player_data and self.player_data["permissions"].get("bridge_station", False)
        if has_bridge_access:
            # Back to station menu button
            back_btn = tk.Button(self.button_frame, text="Back to Station Menu", font=("Arial", 14), width=20, 
                               command=self.show_station_menu)
            back_btn.pack(pady=10)
    
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
        # Check if the door is locked
        door_key = "6,0"  # Bridge door
        if self.player_data.get("ship_map", {}).get(door_key, {}).get("locked", False):
            self.bridge_window.after(10, lambda: messagebox.showinfo("Locked Door", "The door is locked. You must unlock it before leaving.", parent=self.bridge_window))
            # Make sure the window stays on top after dialog
            self.bridge_window.after(20, self.bridge_window.lift)
            self.bridge_window.focus_force()
            return
        
        # Release grab before closing
        self.bridge_window.grab_release()
        
        # Call return callback with player data
        self.return_callback(self.player_data)
        
        # Destroy the window
        self.bridge_window.destroy()

    def show_station_menu(self):
        """Return to main station menu options"""
        # Clear existing buttons
        for widget in self.button_frame.winfo_children():
            widget.destroy()
            
        # Check if user has special access
        has_bridge_access = "permissions" in self.player_data and self.player_data["permissions"].get("bridge_station", False)
        
        if has_bridge_access:
            # Show station access button for authorized personnel
            station_btn = tk.Button(self.button_frame, text="Enter Bridge Station", font=("Arial", 14), width=20, command=self.access_bridge_station)
            station_btn.pack(pady=10)
            
            # Add door lock/unlock button for authorized personnel
            door_btn = tk.Button(self.button_frame, text="Lock/Unlock Door", font=("Arial", 14), width=20, command=self.toggle_door_lock)
            door_btn.pack(pady=10)
            
            # Add "Room Options" button to show regular options
            options_btn = tk.Button(self.button_frame, text="Room Options", font=("Arial", 14), width=20, command=self.show_room_options)
            options_btn.pack(pady=10)
        else:
            # Show regular options for unauthorized personnel
            self.show_room_options()

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
            door_btn = tk.Button(self.button_frame, text="Lock/Unlock Door", font=("Arial", 14), width=20, command=self.toggle_door_lock)
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
        # Clear existing buttons
        for widget in self.button_frame.winfo_children():
            widget.destroy()
            
        # Talk to guard option
        guard_btn = tk.Button(self.button_frame, text="Talk to Security Guard", font=("Arial", 14), width=20, command=self.talk_to_guard)
        guard_btn.pack(pady=10)
        
        # Only show "Back to Station Menu" if player has access
        has_security_access = "permissions" in self.player_data and self.player_data["permissions"].get("security_station", False)
        if has_security_access:
            # Back to station menu button
            back_btn = tk.Button(self.button_frame, text="Back to Station Menu", font=("Arial", 14), width=20, 
                               command=self.show_station_menu)
            back_btn.pack(pady=10)
    
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
        # Check if the door is locked
        door_key = "6,6"  # Security door
        if self.player_data.get("ship_map", {}).get(door_key, {}).get("locked", False):
            self.security_window.after(10, lambda: messagebox.showinfo("Locked Door", "The door is locked. You must unlock it before leaving.", parent=self.security_window))
            # Make sure the window stays on top after dialog
            self.security_window.after(20, self.security_window.lift)
            self.security_window.focus_force()
            return
        
        # Release grab before closing
        self.security_window.grab_release()
        
        # Call return callback with player data
        self.return_callback(self.player_data)
        
        # Destroy the window
        self.security_window.destroy()

    def show_station_menu(self):
        """Return to main station menu options"""
        # Clear existing buttons
        for widget in self.button_frame.winfo_children():
            widget.destroy()
            
        # Check if user has special access
        has_security_access = "permissions" in self.player_data and self.player_data["permissions"].get("security_station", False)
        
        if has_security_access:
            # Show station access button for authorized personnel
            station_btn = tk.Button(self.button_frame, text="Enter Security Station", font=("Arial", 14), width=20, command=self.access_security_station)
            station_btn.pack(pady=10)
            
            # Add door lock/unlock button for authorized personnel
            door_btn = tk.Button(self.button_frame, text="Lock/Unlock Door", font=("Arial", 14), width=20, command=self.toggle_door_lock)
            door_btn.pack(pady=10)
            
            # Add "Room Options" button to show regular options
            options_btn = tk.Button(self.button_frame, text="Room Options", font=("Arial", 14), width=20, command=self.show_room_options)
            options_btn.pack(pady=10)
        else:
            # Show regular options for unauthorized personnel
            self.show_room_options()

class Engineering:
    def __init__(self, parent_window, player_data, return_callback):
        # Create a new toplevel window
        self.engineering_window = tk.Toplevel(parent_window)
        self.engineering_window.title("Engineering Bay")
        self.engineering_window.geometry("800x600")
        self.engineering_window.configure(bg="black")
        
        # Store references
        self.parent_window = parent_window
        self.player_data = player_data
        self.return_callback = return_callback
        
        # Bind window closing
        self.engineering_window.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Ensure this window stays on top
        self.engineering_window.transient(parent_window)
        self.engineering_window.grab_set()
        self.engineering_window.focus_force()
        
        # Center window on screen after window is configured
        self.engineering_window.update_idletasks()
        width = 800
        height = 600
        x = (self.engineering_window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.engineering_window.winfo_screenheight() // 2) - (height // 2)
        self.engineering_window.geometry(f"{width}x{height}+{x}+{y}")
        
        # Title
        room_label = tk.Label(self.engineering_window, text="Station Engineering Bay", font=("Arial", 24), bg="black", fg="white")
        room_label.pack(pady=30)
        
        # Description
        desc_label = tk.Label(self.engineering_window, 
                              text="The engineering bay is filled with equipment and tools. Various machines hum with power, and spare parts are organized on shelves. This is where the station's systems are maintained and repaired.",
                              font=("Arial", 12), bg="black", fg="white", wraplength=600)
        desc_label.pack(pady=10)
        
        # Room actions
        self.button_frame = tk.Frame(self.engineering_window, bg="black")
        self.button_frame.pack(pady=20)
        
        # Check if user has special access (Engineer or Captain)
        has_engineering_access = ("permissions" in self.player_data and self.player_data["permissions"].get("engineering_station", False)) or \
                                 (self.player_data.get("job") == "Engineer") or \
                                 (self.player_data.get("job") == "Captain")
        
        if has_engineering_access:
            # Show station access button for authorized personnel
            station_btn = tk.Button(self.button_frame, text="Enter Engineering Station", font=("Arial", 14), width=20, command=self.access_engineering_station)
            station_btn.pack(pady=10)
            
            # Add door lock/unlock button for authorized personnel
            door_btn = tk.Button(self.button_frame, text="Lock/Unlock Door", font=("Arial", 14), width=20, command=self.toggle_door_lock)
            door_btn.pack(pady=10)
            
            # Add "Room Options" button to show regular options
            options_btn = tk.Button(self.button_frame, text="Room Options", font=("Arial", 14), width=20, command=self.show_room_options)
            options_btn.pack(pady=10)
        else:
            # Show regular options for unauthorized personnel
            self.show_room_options()
        
        # Exit button
        exit_btn = tk.Button(self.engineering_window, text="Exit Room", font=("Arial", 14), width=15, command=self.on_closing)
        exit_btn.pack(pady=20)
    
    def show_room_options(self):
        """Show regular room options that all players can access"""
        # Clear existing buttons
        for widget in self.button_frame.winfo_children():
            widget.destroy()
            
        # Engineering options
        examine_btn = tk.Button(self.button_frame, text="Examine Tools", font=("Arial", 14), width=20, command=self.examine_tools)
        examine_btn.pack(pady=10)
        
        # Only show "Back to Station Menu" if player has access
        has_engineering_access = ("permissions" in self.player_data and self.player_data["permissions"].get("engineering_station", False)) or \
                                 (self.player_data.get("job") == "Engineer") or \
                                 (self.player_data.get("job") == "Captain")
        if has_engineering_access:
            # Back to station menu button
            back_btn = tk.Button(self.button_frame, text="Back to Station Menu", font=("Arial", 14), width=20, 
                               command=self.show_station_menu)
            back_btn.pack(pady=10)
    
    def examine_tools(self):
        # Show dialog with the room window as parent to keep focus within the room
        self.engineering_window.after(10, lambda: messagebox.showinfo("Engineering Tools", "You see various tools for repairing and maintaining station systems. Without proper training, their use is not advised.", parent=self.engineering_window))
        # Make sure the window stays on top after dialog
        self.engineering_window.after(20, self.engineering_window.lift)
        self.engineering_window.focus_force()
    
    def access_engineering_station(self):
        # Show access confirmation for authorized personnel
        self.engineering_window.after(10, lambda: messagebox.showinfo("Engineering Station", "Access granted. Welcome to the Engineering Station.", parent=self.engineering_window))
        # Make sure the window stays on top after dialog
        self.engineering_window.after(20, self.engineering_window.lift)
        self.engineering_window.focus_force()
    
    def toggle_door_lock(self):
        # Get the door location key
        door_key = "6,3"
        
        # Get the ship map from player data
        if "ship_map" not in self.player_data:
            self.engineering_window.after(10, lambda: messagebox.showinfo("Door Control", "Unable to access door control system.", parent=self.engineering_window))
            return
            
        ship_map = self.player_data["ship_map"]
        if door_key not in ship_map:
            self.engineering_window.after(10, lambda: messagebox.showinfo("Door Control", "Unable to access door control system.", parent=self.engineering_window))
            return
            
        # Toggle the door lock
        if ship_map[door_key].get("locked", False):
            ship_map[door_key]["locked"] = False
            ship_map[door_key]["desc"] = "The station's engineering and maintenance center. The door is unlocked."
            self.engineering_window.after(10, lambda: messagebox.showinfo("Door Control", "The Engineering Bay door has been unlocked.", parent=self.engineering_window))
        else:
            ship_map[door_key]["locked"] = True
            ship_map[door_key]["desc"] = "The station's engineering and maintenance center. The door is locked."
            self.engineering_window.after(10, lambda: messagebox.showinfo("Door Control", "The Engineering Bay door has been locked.", parent=self.engineering_window))
        
        # Update ship map in player data
        self.player_data["ship_map"] = ship_map
        
        # Make sure the window stays on top after dialog
        self.engineering_window.after(20, self.engineering_window.lift)
        self.engineering_window.focus_force()
    
    def on_closing(self):
        # Check if the door is locked
        door_key = "6,3"  # Engineering door
        if self.player_data.get("ship_map", {}).get(door_key, {}).get("locked", False):
            self.engineering_window.after(10, lambda: messagebox.showinfo("Locked Door", "The door is locked. You must unlock it before leaving.", parent=self.engineering_window))
            # Make sure the window stays on top after dialog
            self.engineering_window.after(20, self.engineering_window.lift)
            self.engineering_window.focus_force()
            return
        
        # Release grab before closing
        self.engineering_window.grab_release()
        
        # Call return callback with player data
        self.return_callback(self.player_data)
        
        # Destroy the window
        self.engineering_window.destroy()

    def show_station_menu(self):
        """Return to main station menu options"""
        # Clear existing buttons
        for widget in self.button_frame.winfo_children():
            widget.destroy()
            
        # Check if user has special access (Engineer or Captain)
        has_engineering_access = ("permissions" in self.player_data and self.player_data["permissions"].get("engineering_station", False)) or \
                                 (self.player_data.get("job") == "Engineer") or \
                                 (self.player_data.get("job") == "Captain")
        
        if has_engineering_access:
            # Show station access button for authorized personnel
            station_btn = tk.Button(self.button_frame, text="Enter Engineering Station", font=("Arial", 14), width=20, command=self.access_engineering_station)
            station_btn.pack(pady=10)
            
            # Add door lock/unlock button for authorized personnel
            door_btn = tk.Button(self.button_frame, text="Lock/Unlock Door", font=("Arial", 14), width=20, command=self.toggle_door_lock)
            door_btn.pack(pady=10)
            
            # Add "Room Options" button to show regular options
            options_btn = tk.Button(self.button_frame, text="Room Options", font=("Arial", 14), width=20, command=self.show_room_options)
            options_btn.pack(pady=10)
        else:
            # Show regular options for unauthorized personnel
            self.show_room_options() 