import tkinter as tk
from tkinter import ttk, messagebox
import datetime
import random

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
        
        # Check if user has special access (Captain or HoP)
        is_captain = self.player_data.get("job") == "Captain"
        is_hop = self.player_data.get("job") == "Head of Personnel"
        has_captain_access = is_captain or "permissions" in self.player_data and self.player_data["permissions"].get("bridge_station", False)
        has_hop_access = is_captain or is_hop or "permissions" in self.player_data and self.player_data["permissions"].get("hop_station", False)
        
        if has_captain_access or has_hop_access:
            # Show the appropriate station access buttons
            if has_captain_access:
                captain_btn = tk.Button(self.button_frame, text="Enter Captain's Station", font=("Arial", 14), width=20, command=self.access_captain_station)
                captain_btn.pack(pady=10)
            
            if has_hop_access:
                hop_btn = tk.Button(self.button_frame, text="Enter HoP's Station", font=("Arial", 14), width=20, command=self.access_hop_station)
                hop_btn.pack(pady=10)
            
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
        
        # Only show "Back to Station Menu" if player has special access
        is_captain = self.player_data.get("job") == "Captain"
        is_hop = self.player_data.get("job") == "Head of Personnel"
        has_captain_access = is_captain or "permissions" in self.player_data and self.player_data["permissions"].get("bridge_station", False)
        has_hop_access = is_captain or is_hop or "permissions" in self.player_data and self.player_data["permissions"].get("hop_station", False)
        
        if has_captain_access or has_hop_access:
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
    
    def access_captain_station(self):
        """Access the Captain's Station interface"""
        # Show access confirmation for authorized personnel
        self.bridge_window.after(10, lambda: messagebox.showinfo("Captain's Station", "Access granted. Welcome to the Captain's Station.", parent=self.bridge_window))
        
        # Clear existing buttons
        for widget in self.button_frame.winfo_children():
            widget.destroy()
            
        # Add captain station options
        station_label = tk.Label(self.button_frame, text="Captain's Station", font=("Arial", 16, "bold"), bg="black", fg="white")
        station_label.pack(pady=10)
        
        # Add station control buttons
        status_btn = tk.Button(self.button_frame, text="Station Status", font=("Arial", 14), width=20, 
                             command=lambda: messagebox.showinfo("Station Status", "All systems nominal. No critical alerts.", parent=self.bridge_window))
        status_btn.pack(pady=5)
        
        security_btn = tk.Button(self.button_frame, text="Security Alerts", font=("Arial", 14), width=20, 
                               command=lambda: messagebox.showinfo("Security Alerts", "No security alerts reported.", parent=self.bridge_window))
        security_btn.pack(pady=5)
        
        manifest_btn = tk.Button(self.button_frame, text="Crew Manifest", font=("Arial", 14), width=20, command=self.show_crew_manifest)
        manifest_btn.pack(pady=5)
        
        emergency_btn = tk.Button(self.button_frame, text="Emergency Protocols", font=("Arial", 14), width=20, 
                                command=lambda: messagebox.showinfo("Emergency Protocols", "Emergency protocols ready for activation if needed.", parent=self.bridge_window))
        emergency_btn.pack(pady=5)
        
        # Back button
        back_btn = tk.Button(self.button_frame, text="Back to Bridge Menu", font=("Arial", 14), width=20, command=self.show_station_menu)
        back_btn.pack(pady=15)
        
        # Make sure the window stays on top after dialog
        self.bridge_window.after(20, self.bridge_window.lift)
        self.bridge_window.focus_force()
    
    def access_hop_station(self):
        """Access the Head of Personnel (HoP) Station interface"""
        # Show access confirmation for authorized personnel
        self.bridge_window.after(10, lambda: messagebox.showinfo("HoP Station", "Access granted. Welcome to the Head of Personnel Station.", parent=self.bridge_window))
        
        # Clear existing buttons
        for widget in self.button_frame.winfo_children():
            widget.destroy()
            
        # Add HoP station options
        station_label = tk.Label(self.button_frame, text="Head of Personnel Station", font=("Arial", 16, "bold"), bg="black", fg="white")
        station_label.pack(pady=10)
        
        # Add station control buttons
        manifest_btn = tk.Button(self.button_frame, text="Crew Manifest", font=("Arial", 14), width=20, command=self.show_crew_manifest)
        manifest_btn.pack(pady=5)
        
        assignments_btn = tk.Button(self.button_frame, text="Job Assignments", font=("Arial", 14), width=20, 
                                  command=lambda: messagebox.showinfo("Job Assignments", "All current job positions are filled.", parent=self.bridge_window))
        assignments_btn.pack(pady=5)
        
        access_btn = tk.Button(self.button_frame, text="Access Control", font=("Arial", 14), width=20, 
                             command=lambda: messagebox.showinfo("Access Control", "Access control system ready. No pending requests.", parent=self.bridge_window))
        access_btn.pack(pady=5)
        
        records_btn = tk.Button(self.button_frame, text="Personnel Records", font=("Arial", 14), width=20, 
                              command=lambda: messagebox.showinfo("Personnel Records", "Personnel records database online. All records up to date.", parent=self.bridge_window))
        records_btn.pack(pady=5)
        
        # Back button
        back_btn = tk.Button(self.button_frame, text="Back to Bridge Menu", font=("Arial", 14), width=20, command=self.show_station_menu)
        back_btn.pack(pady=15)
        
        # Make sure the window stays on top after dialog
        self.bridge_window.after(20, self.bridge_window.lift)
        self.bridge_window.focus_force()
    
    def show_crew_manifest(self):
        """Display the crew manifest with department listings"""
        # Create a new toplevel window
        manifest_window = tk.Toplevel(self.bridge_window)
        manifest_window.title("Crew Manifest")
        manifest_window.geometry("600x500")
        manifest_window.configure(bg="black")
        manifest_window.transient(self.bridge_window)
        manifest_window.grab_set()
        
        # Center the popup
        manifest_window.update_idletasks()
        width = 600
        height = 500
        x = (manifest_window.winfo_screenwidth() // 2) - (width // 2)
        y = (manifest_window.winfo_screenheight() // 2) - (height // 2)
        manifest_window.geometry(f"{width}x{height}+{x}+{y}")
        
        # Title
        title_label = tk.Label(manifest_window, text="Station Crew Manifest", font=("Arial", 18, "bold"), bg="black", fg="white")
        title_label.pack(pady=10)
        
        # Create scrollable frame for crew list
        frame = tk.Frame(manifest_window, bg="black")
        frame.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)
        
        # Add scrollbar
        scrollbar = tk.Scrollbar(frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Create text widget for manifest
        manifest_text = tk.Text(frame, bg="black", fg="white", font=("Arial", 12),
                             width=50, height=20, yscrollcommand=scrollbar.set, wrap=tk.WORD)
        manifest_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=manifest_text.yview)
        
        # Configure text tags for formatting
        manifest_text.tag_configure("header", font=("Arial", 14, "bold"), foreground="yellow")
        manifest_text.tag_configure("department", font=("Arial", 12, "bold"), foreground="light blue")
        manifest_text.tag_configure("name", font=("Arial", 11))
        manifest_text.tag_configure("player", font=("Arial", 11, "bold"), foreground="light green")
        
        # Create a structured crew manifest
        manifest_text.insert(tk.END, "STATION CREW MANIFEST\n", "header")
        manifest_text.insert(tk.END, "====================\n\n", "header")
        
        # Command Department
        manifest_text.insert(tk.END, "COMMAND:\n", "department")
        
        # Determine if player is in Command department
        player_name = self.player_data.get("name", "Unknown")
        player_job = self.player_data.get("job", "Unknown")
        
        if player_job == "Captain":
            manifest_text.insert(tk.END, f"- Captain: {player_name} (YOU)\n", "player")
        else:
            manifest_text.insert(tk.END, "- Captain: James Anderson\n", "name")
            
        if player_job == "Head of Personnel":
            manifest_text.insert(tk.END, f"- Head of Personnel: {player_name} (YOU)\n\n", "player")
        else:
            manifest_text.insert(tk.END, "- Head of Personnel: Sarah Chen\n\n", "name")
        
        # Security Department
        manifest_text.insert(tk.END, "SECURITY:\n", "department")
        
        if player_job == "Security Guard":
            manifest_text.insert(tk.END, f"- Security Guard: {player_name} (YOU)\n\n", "player")
        else:
            manifest_text.insert(tk.END, "- Security Guard: Marcus Reynolds\n\n", "name")
        
        # Medical Department
        manifest_text.insert(tk.END, "MEDICAL:\n", "department")
        
        if player_job == "Doctor":
            manifest_text.insert(tk.END, f"- Doctor: {player_name} (YOU)\n\n", "player")
        else:
            manifest_text.insert(tk.END, "- Doctor: Elena Vasquez\n\n", "name")
        
        # Engineering Department
        manifest_text.insert(tk.END, "ENGINEERING:\n", "department")
        
        if player_job == "Engineer":
            manifest_text.insert(tk.END, f"- Engineer: {player_name} (YOU)\n\n", "player")
        else:
            manifest_text.insert(tk.END, "- Engineer: Raj Patel\n\n", "name")
        
        # Service Department
        manifest_text.insert(tk.END, "SERVICE:\n", "department")
        
        if player_job == "Bartender":
            manifest_text.insert(tk.END, f"- Bartender: {player_name} (YOU)\n\n", "player")
        else:
            manifest_text.insert(tk.END, "- Bartender: Dana Williams\n\n", "name")
        
        # Civilian Department
        manifest_text.insert(tk.END, "CIVILIAN:\n", "department")
        
        if player_job == "Staff Assistant":
            manifest_text.insert(tk.END, f"- Staff Assistant: {player_name} (YOU)\n\n", "player")
        else:
            manifest_text.insert(tk.END, "- Staff Assistant: Jordan Lee\n\n", "name")
        
        # Make text widget read-only
        manifest_text.config(state=tk.DISABLED)
        
        # Mouse wheel binding for scrolling
        def _on_manifest_mousewheel(event):
            try:
                manifest_text.yview_scroll(int(-1*(event.delta/120)), "units")
            except tk.TclError:
                pass  # Ignore errors if the text widget was destroyed
        
        # Bind mousewheel to manifest text
        manifest_window.bind("<MouseWheel>", _on_manifest_mousewheel)
        
        # Override destroy method to cleanup bindings
        orig_destroy = manifest_window.destroy
        def _destroy_and_cleanup():
            try:
                manifest_window.unbind("<MouseWheel>")
            except:
                pass
            orig_destroy()
        
        manifest_window.destroy = _destroy_and_cleanup
        
        # Close button
        close_btn = tk.Button(manifest_window, text="Close", font=("Arial", 12), command=manifest_window.destroy)
        close_btn.pack(pady=10)
    
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
        is_captain = self.player_data.get("job") == "Captain"
        is_hop = self.player_data.get("job") == "Head of Personnel"
        has_captain_access = is_captain or "permissions" in self.player_data and self.player_data["permissions"].get("bridge_station", False)
        has_hop_access = is_captain or is_hop or "permissions" in self.player_data and self.player_data["permissions"].get("hop_station", False)
        
        if has_captain_access or has_hop_access:
            # Show the appropriate station access buttons
            if has_captain_access:
                captain_btn = tk.Button(self.button_frame, text="Enter Captain's Station", font=("Arial", 14), width=20, command=self.access_captain_station)
                captain_btn.pack(pady=10)
            
            if has_hop_access:
                hop_btn = tk.Button(self.button_frame, text="Enter HoP's Station", font=("Arial", 14), width=20, command=self.access_hop_station)
                hop_btn.pack(pady=10)
            
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
        
        # Define engineering tools
        self.tools_inventory = [
            {"name": "Wrench", "description": "Standard tool for fastening and unfastening bolts and nuts."},
            {"name": "Screwdriver Set", "description": "Multi-head screwdriver for various screw types."},
            {"name": "Wire Cutters", "description": "Tool for cutting and stripping wires safely."},
            {"name": "Multimeter", "description": "Device for measuring voltage, current, and resistance."},
            {"name": "Welding Tool", "description": "For joining metal components."},
            {"name": "Plasma Cutter", "description": "Precision cutting tool for metal panels."},
            {"name": "Circuit Analyzer", "description": "Diagnostic tool for electronic circuits."},
            {"name": "Power Cell Charger", "description": "Recharges depleted power cells."},
            {"name": "Insulated Gloves", "description": "Protection when working with electrical systems."},
            {"name": "Atmospheric Scanner", "description": "Monitors air quality and composition."}
        ]
        
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
        """Display all engineering tools in a locker-like interface"""
        # Create a new top-level window
        tools_popup = tk.Toplevel(self.engineering_window)
        tools_popup.title("Engineering Tools")
        tools_popup.geometry("700x500")
        tools_popup.configure(bg="black")
        tools_popup.transient(self.engineering_window)
        tools_popup.grab_set()
        
        # Center the popup
        tools_popup.update_idletasks()
        width = 700
        height = 500
        x = (tools_popup.winfo_screenwidth() // 2) - (width // 2)
        y = (tools_popup.winfo_screenheight() // 2) - (height // 2)
        tools_popup.geometry(f"{width}x{height}+{x}+{y}")
        
        # Title
        title_label = tk.Label(tools_popup, text="Engineering Tools", font=("Arial", 18), bg="black", fg="white")
        title_label.pack(pady=10)
        
        # Description
        desc_label = tk.Label(tools_popup, text="The tool cabinet contains specialized equipment for maintaining the station's systems.", 
                            font=("Arial", 12), bg="black", fg="white", wraplength=600)
        desc_label.pack(pady=10)
        
        # Create scrollable frame for tools
        tools_frame = tk.Frame(tools_popup, bg="black")
        tools_frame.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)
        
        # Add scrollbar
        scrollbar = tk.Scrollbar(tools_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Create canvas for scrolling
        tools_canvas = tk.Canvas(tools_frame, bg="black", highlightthickness=0)
        tools_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Configure scrollbar
        scrollbar.config(command=tools_canvas.yview)
        tools_canvas.configure(yscrollcommand=scrollbar.set)
        
        # Create frame to hold the tools
        tools_list_frame = tk.Frame(tools_canvas, bg="black")
        
        # Create window in canvas
        tools_canvas.create_window((0, 0), window=tools_list_frame, anchor="nw")
        
        # Populate tools
        for i, tool in enumerate(self.tools_inventory):
            # Create a frame for each tool
            tool_frame = tk.Frame(tools_list_frame, bg="dark gray", bd=2, relief=tk.RAISED)
            tool_frame.pack(fill=tk.X, pady=5, padx=10)
            
            # Tool info
            name_label = tk.Label(tool_frame, text=tool["name"], font=("Arial", 12, "bold"), bg="dark gray")
            name_label.pack(side=tk.TOP, anchor="w", padx=10, pady=(5, 0))
            
            desc_label = tk.Label(tool_frame, text=tool["description"], font=("Arial", 10), 
                               bg="dark gray", wraplength=600, justify=tk.LEFT)
            desc_label.pack(side=tk.TOP, anchor="w", padx=10, pady=(0, 5))
            
            # Add a context-sensitive button based on player job
            if self.player_data.get("job") in ["Engineer", "Captain"]:
                use_btn = tk.Button(tool_frame, text="Use Tool", font=("Arial", 10),
                                 command=lambda t=tool["name"]: self.use_tool(t))
                use_btn.pack(side=tk.RIGHT, padx=10, pady=5)
            else:
                examine_btn = tk.Button(tool_frame, text="Examine", font=("Arial", 10),
                                     command=lambda t=tool["name"]: self.examine_tool(t))
                examine_btn.pack(side=tk.RIGHT, padx=10, pady=5)
        
        # Update the scrollregion
        tools_list_frame.update_idletasks()
        tools_canvas.config(scrollregion=tools_canvas.bbox("all"))
        
        # Mouse wheel scrolling
        def _on_mousewheel(event):
            try:
                tools_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
            except tk.TclError:
                pass
        
        tools_popup.bind("<MouseWheel>", _on_mousewheel)
        
        # Override destroy method to unbind scrolling
        orig_destroy = tools_popup.destroy
        def _destroy_and_cleanup():
            try:
                tools_popup.unbind("<MouseWheel>")
            except:
                pass
            orig_destroy()
        
        tools_popup.destroy = _destroy_and_cleanup
        
        # Close button
        close_btn = tk.Button(tools_popup, text="Close", font=("Arial", 12), command=tools_popup.destroy)
        close_btn.pack(pady=10)
    
    def use_tool(self, tool_name):
        """Use a specific engineering tool (for authorized personnel)"""
        # Show dialog with the tool effect
        message = f"You use the {tool_name} to perform maintenance on nearby equipment."
        
        # Add a random successful outcome
        outcomes = [
            "You successfully calibrate the system.",
            "The equipment is now functioning at optimal levels.",
            "You've improved the efficiency by 12%.",
            "Potential issues have been prevented through your maintenance.",
            "The diagnostic check reveals no further problems."
        ]
        
        message += f"\n\n{random.choice(outcomes)}"
        
        self.engineering_window.after(10, lambda: messagebox.showinfo(f"Using {tool_name}", message, parent=self.engineering_window))
        
        # Make sure the window stays on top after dialog
        self.engineering_window.after(20, self.engineering_window.lift)
        self.engineering_window.focus_force()
    
    def examine_tool(self, tool_name):
        """Examine a tool without using it (for non-engineers)"""
        message = f"You examine the {tool_name}, but aren't sure how to use it properly without engineering training."
        self.engineering_window.after(10, lambda: messagebox.showinfo(f"Examining {tool_name}", message, parent=self.engineering_window))
        
        # Make sure the window stays on top after dialog
        self.engineering_window.after(20, self.engineering_window.lift)
        self.engineering_window.focus_force()
    
    def access_engineering_station(self):
        # Show access confirmation for authorized personnel
        self.engineering_window.after(10, lambda: messagebox.showinfo("Engineering Station", "Access granted. Welcome to the Engineering Station.", parent=self.engineering_window))
        
        # Clear existing buttons
        for widget in self.button_frame.winfo_children():
            widget.destroy()
            
        # Add engineering station options
        station_label = tk.Label(self.button_frame, text="Engineering Station Controls", font=("Arial", 16, "bold"), bg="black", fg="white")
        station_label.pack(pady=10)
        
        # System access buttons
        power_btn = tk.Button(self.button_frame, text="Power Management", font=("Arial", 14), width=20, command=lambda: messagebox.showinfo("Power Management", "Station power systems are operating within normal parameters.", parent=self.engineering_window))
        power_btn.pack(pady=5)
        
        atmos_btn = tk.Button(self.button_frame, text="Atmosphere Controls", font=("Arial", 14), width=20, command=lambda: messagebox.showinfo("Atmosphere Controls", "Life support systems functioning properly. Oxygen levels: 21%, Pressure: 101 kPa", parent=self.engineering_window))
        atmos_btn.pack(pady=5)
        
        toolbox_btn = tk.Button(self.button_frame, text="Access Toolbox", font=("Arial", 14), width=20, command=self.access_toolbox)
        toolbox_btn.pack(pady=5)
        
        back_btn = tk.Button(self.button_frame, text="Back to Main Menu", font=("Arial", 14), width=20, command=self.show_station_menu)
        back_btn.pack(pady=15)
        
        # Make sure the window stays on top after dialog
        self.engineering_window.after(20, self.engineering_window.lift)
        self.engineering_window.focus_force()
    
    def access_toolbox(self):
        """Access the engineering toolbox with specialized tools"""
        # Check if user has special access (Engineer or Captain)
        has_engineering_access = ("permissions" in self.player_data and self.player_data["permissions"].get("engineering_station", False)) or \
                                (self.player_data.get("job") == "Engineer") or \
                                (self.player_data.get("job") == "Captain")
        
        if has_engineering_access:
            # Show specialized toolbox for authorized personnel
            toolbox_window = tk.Toplevel(self.engineering_window)
            toolbox_window.title("Engineering Toolbox")
            toolbox_window.geometry("600x500")
            toolbox_window.configure(bg="black")
            
            # Ensure this window stays on top
            toolbox_window.transient(self.engineering_window)
            toolbox_window.grab_set()
            
            # Title
            title_label = tk.Label(toolbox_window, text="Specialized Engineering Tools", font=("Arial", 18, "bold"), bg="black", fg="white")
            title_label.pack(pady=15)
            
            # Description
            desc_label = tk.Label(toolbox_window, text="This secure toolbox contains specialized equipment for station maintenance and emergency repairs.", 
                                 font=("Arial", 12), bg="black", fg="white", wraplength=500)
            desc_label.pack(pady=10)
            
            # Create a frame for the scrollable content
            tools_outer_frame = tk.Frame(toolbox_window, bg="black")
            tools_outer_frame.pack(pady=10, fill=tk.BOTH, expand=True)
            
            # Add scrollbar to the frame
            scrollbar = tk.Scrollbar(tools_outer_frame)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            
            # Create canvas for scrolling
            tools_canvas = tk.Canvas(tools_outer_frame, bg="black", highlightthickness=0)
            tools_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            
            # Configure scrollbar to work with canvas
            scrollbar.config(command=tools_canvas.yview)
            tools_canvas.configure(yscrollcommand=scrollbar.set)
            
            # Create inner frame for tools
            tools_frame = tk.Frame(tools_canvas, bg="black")
            
            # Add the inner frame to the canvas
            canvas_window = tools_canvas.create_window((0, 0), window=tools_frame, anchor=tk.NW)
            
            # Specialized tools list
            specialized_tools = [
                {"name": "Power Coupling Optimizer", "description": "Balances load across power distribution networks."},
                {"name": "Quantum Harmonizer", "description": "Aligns phase shifts in sensitive equipment."},
                {"name": "Plasma Flow Regulator", "description": "Controls plasma injection rates in the reactor core."},
                {"name": "Singularity Containment Monitor", "description": "Monitors field stability in high-energy systems."},
                {"name": "Thermal Dampening Coils", "description": "Reduces heat signatures in sensitive areas."},
                {"name": "Antimatter Containment Field", "description": "Maintains the integrity of antimatter storage units."},
                {"name": "Subspace Field Modulator", "description": "Calibrates subspace field generators for communications."},
                {"name": "Graviton Pulse Emitter", "description": "Creates localized gravity fields for specialized repairs."},
                {"name": "Tachyon Detection Grid", "description": "Scans for tachyon particles that may indicate temporal anomalies."},
                {"name": "Neural Interface Adapter", "description": "Allows direct neural connection to station systems for diagnostics."}
            ]
            
            # Add tools to frame
            for i, tool in enumerate(specialized_tools):
                tool_frame = tk.Frame(tools_frame, bg="#222222", bd=1, relief=tk.RIDGE)
                tool_frame.pack(fill=tk.X, padx=20, pady=5)
                
                name_label = tk.Label(tool_frame, text=tool["name"], font=("Arial", 14, "bold"), bg="#222222", fg="#00CCFF")
                name_label.pack(anchor="w", padx=10, pady=5)
                
                desc_label = tk.Label(tool_frame, text=tool["description"], font=("Arial", 12), bg="#222222", fg="white", wraplength=500)
                desc_label.pack(anchor="w", padx=10, pady=5)
                
                use_btn = tk.Button(tool_frame, text="Use Tool", font=("Arial", 12), bg="#555555", fg="white", 
                                command=lambda t=tool["name"]: messagebox.showinfo("Tool Usage", f"You used the {t} to optimize station systems.", parent=toolbox_window))
                use_btn.pack(anchor="e", padx=10, pady=5)
            
            # Update scrollregion when the frame changes size
            def configure_scroll_region(event):
                tools_canvas.configure(scrollregion=tools_canvas.bbox("all"))
                tools_canvas.itemconfig(canvas_window, width=tools_canvas.winfo_width())
            
            tools_frame.bind("<Configure>", configure_scroll_region)
            tools_canvas.bind("<Configure>", lambda e: tools_canvas.itemconfig(canvas_window, width=e.width))
            
            # Function to handle mousewheel scrolling
            def on_mousewheel(event):
                try:
                    # Windows style scrolling
                    tools_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
                except Exception as e:
                    try:
                        # Linux style scrolling
                        if event.num == 4:
                            tools_canvas.yview_scroll(-1, "units")
                        elif event.num == 5:
                            tools_canvas.yview_scroll(1, "units")
                    except:
                        pass  # Ignore errors if the canvas was destroyed
            
            # Bind the mousewheel event to the canvas and window
            tools_canvas.bind("<MouseWheel>", on_mousewheel)
            tools_canvas.bind("<Button-4>", on_mousewheel)
            tools_canvas.bind("<Button-5>", on_mousewheel)
            
            toolbox_window.bind("<MouseWheel>", on_mousewheel)
            toolbox_window.bind("<Button-4>", on_mousewheel)
            toolbox_window.bind("<Button-5>", on_mousewheel)
            
            # Close button
            close_btn = tk.Button(toolbox_window, text="Close Toolbox", font=("Arial", 14), bg="#333333", fg="white",
                                command=toolbox_window.destroy)
            close_btn.pack(pady=15)
            
            # Make sure to unbind events when window is closed
            orig_destroy = toolbox_window.destroy
            def _destroy_and_cleanup():
                try:
                    toolbox_window.unbind("<MouseWheel>")
                    toolbox_window.unbind("<Button-4>")
                    toolbox_window.unbind("<Button-5>")
                except:
                    pass
                orig_destroy()
            
            toolbox_window.destroy = _destroy_and_cleanup
            
        else:
            # Warning for unauthorized personnel
            warning_message = "WARNING: These specialized engineering tools should only be handled by trained personnel. Improper use could result in station damage, injury, or death. Access restricted to Engineering staff and Command personnel only."
            messagebox.showwarning("Access Restricted", warning_message, parent=self.engineering_window)
            
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

class Bar:
    def __init__(self, parent_window, player_data, return_callback):
        # Create a new toplevel window
        self.bar_window = tk.Toplevel(parent_window)
        self.bar_window.title("Bar")
        self.bar_window.geometry("800x600")
        self.bar_window.configure(bg="black")
        
        # Store references
        self.parent_window = parent_window
        self.player_data = player_data
        self.return_callback = return_callback
        
        # Define drinks available in the bar
        self.drinks_menu = {
            "Beer": {"price": 10, "desc": "A refreshing glass of regular beer."},
            "Whiskey": {"price": 20, "desc": "A shot of strong whiskey."},
            "Wine": {"price": 15, "desc": "A fine glass of red wine."},
            "Vodka": {"price": 15, "desc": "A shot of clear, strong vodka."},
            "Gin": {"price": 15, "desc": "A botanical spirit with a distinctive flavor."},
            "Rum": {"price": 15, "desc": "A sweet spirit distilled from sugarcane."},
            "Tequila": {"price": 18, "desc": "A spirit made from the blue agave plant."},
            "Brandy": {"price": 22, "desc": "A spirit distilled from wine or fermented fruit juice."},
            "Scotch": {"price": 25, "desc": "A smoky whisky from Scotland."},
            "Orange Juice": {"price": 5, "desc": "A glass of fresh orange juice."},
            "Cranberry Juice": {"price": 5, "desc": "Tart and refreshing red juice."},
            "Pineapple Juice": {"price": 6, "desc": "Sweet tropical juice."},
            "Tonic Water": {"price": 4, "desc": "Carbonated water with quinine."},
            "Soda Water": {"price": 3, "desc": "Simple carbonated water."},
            "Cola": {"price": 4, "desc": "A sweet carbonated soft drink."},
            "Lemon Juice": {"price": 4, "desc": "Fresh, sour citrus juice."},
            "Lime Juice": {"price": 4, "desc": "Zesty green citrus juice."},
            "Grenadine": {"price": 5, "desc": "Sweet red syrup made from pomegranate."},
            "Water": {"price": 1, "desc": "A glass of water. Refreshing and healthy."}
        }
        
        # Define mixed drinks that bartenders can make
        self.mixed_drinks = {
            "Screwdriver": {
                "ingredients": ["Vodka", "Orange Juice"],
                "price": 25,
                "desc": "A classic mix of vodka and orange juice."
            },
            "Gin and Tonic": {
                "ingredients": ["Gin", "Tonic Water"],
                "price": 20,
                "desc": "A refreshing mix of gin and tonic water."
            },
            "Rum and Cola": {
                "ingredients": ["Rum", "Cola"],
                "price": 20,
                "desc": "A sweet mix of rum and cola."
            },
            "Whiskey Sour": {
                "ingredients": ["Whiskey", "Lemon Juice", "Sugar"],
                "price": 28,
                "desc": "A perfect balance of sour and sweet with whiskey."
            },
            "Margarita": {
                "ingredients": ["Tequila", "Lime Juice", "Triple Sec"],
                "price": 30,
                "desc": "A tangy, refreshing cocktail with a salt rim."
            },
            "Bloody Mary": {
                "ingredients": ["Vodka", "Tomato Juice", "Hot Sauce", "Worcestershire Sauce"],
                "price": 28,
                "desc": "A savory, spicy morning cocktail."
            },
            "Mojito": {
                "ingredients": ["Rum", "Lime Juice", "Mint", "Sugar", "Soda Water"],
                "price": 32,
                "desc": "A refreshing minty cocktail from Cuba."
            },
            "Piña Colada": {
                "ingredients": ["Rum", "Coconut Cream", "Pineapple Juice"],
                "price": 30,
                "desc": "A tropical blend that tastes like vacation."
            },
            "Cosmopolitan": {
                "ingredients": ["Vodka", "Triple Sec", "Cranberry Juice", "Lime Juice"],
                "price": 30,
                "desc": "A sophisticated, slightly tart cocktail."
            },
            "Old Fashioned": {
                "ingredients": ["Whiskey", "Bitters", "Sugar", "Water"],
                "price": 32,
                "desc": "A timeless cocktail that never goes out of style."
            },
            "Negroni": {
                "ingredients": ["Gin", "Vermouth", "Campari"],
                "price": 30,
                "desc": "A perfectly balanced bitter and sweet aperitif."
            },
            "Manhattan": {
                "ingredients": ["Whiskey", "Vermouth", "Bitters"],
                "price": 32,
                "desc": "A sophisticated whiskey cocktail."
            },
            "Mai Tai": {
                "ingredients": ["Rum", "Lime Juice", "Orange Curacao", "Orgeat Syrup"],
                "price": 35,
                "desc": "A complex tropical rum cocktail."
            },
            "Daiquiri": {
                "ingredients": ["Rum", "Lime Juice", "Sugar"],
                "price": 28,
                "desc": "A simple, refreshing rum cocktail."
            },
            "Tom Collins": {
                "ingredients": ["Gin", "Lemon Juice", "Sugar", "Soda Water"],
                "price": 28,
                "desc": "A refreshing gin cocktail served in a tall glass."
            },
            "Singapore Sling": {
                "ingredients": ["Gin", "Cherry Brandy", "Pineapple Juice", "Lime Juice", "Grenadine"],
                "price": 35,
                "desc": "A complex, fruity gin cocktail."
            },
            "Long Island Iced Tea": {
                "ingredients": ["Vodka", "Gin", "Rum", "Tequila", "Triple Sec", "Lemon Juice", "Cola"],
                "price": 40,
                "desc": "A potent mix of multiple spirits with a cola finish."
            },
            "Space Blaster": {
                "ingredients": ["Vodka", "Blue Curacao", "Sprite", "Lemon Juice"],
                "price": 35,
                "desc": "A station specialty with an electric blue color."
            },
            "Quantum Fizz": {
                "ingredients": ["Gin", "Lime Juice", "Sugar", "Mint", "Helium Gas"],
                "price": 38,
                "desc": "A unique drink that temporarily changes your voice."
            },
            "Nebula Cloud": {
                "ingredients": ["Whiskey", "Honey", "Dry Ice", "Cinnamon"],
                "price": 42,
                "desc": "A smoky cocktail that mimics a space nebula."
            }
        }
        
        # Track bartender mode
        self.bartender_mode = False
        
        # Define ingredients available for bartending
        self.available_ingredients = [
            # Spirits
            "Vodka", "Gin", "Rum", "Whiskey", "Tequila", "Brandy", "Scotch", 
            # Mixers and Juices
            "Orange Juice", "Cranberry Juice", "Pineapple Juice", "Tomato Juice",
            "Tonic Water", "Soda Water", "Cola", "Ginger Ale", "Sprite",
            # Modifiers
            "Lemon Juice", "Lime Juice", "Sugar", "Salt", "Honey", 
            "Triple Sec", "Blue Curacao", "Orange Curacao", "Grenadine",
            "Bitters", "Vermouth", "Campari", "Cherry Brandy",
            # Special ingredients
            "Mint", "Coconut Cream", "Hot Sauce", "Worcestershire Sauce", 
            "Cinnamon", "Orgeat Syrup", "Dry Ice", "Helium Gas"
        ]
        
        # Bind window closing
        self.bar_window.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Ensure this window stays on top
        self.bar_window.transient(parent_window)
        self.bar_window.grab_set()
        self.bar_window.focus_force()
        
        # Center window on screen after window is configured
        self.bar_window.update_idletasks()
        width = 800
        height = 600
        x = (self.bar_window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.bar_window.winfo_screenheight() // 2) - (height // 2)
        self.bar_window.geometry(f"{width}x{height}+{x}+{y}")
        
        # Title
        room_label = tk.Label(self.bar_window, text="Station Bar", font=("Arial", 24), bg="black", fg="white")
        room_label.pack(pady=30)
        
        # Description
        desc_label = tk.Label(self.bar_window, 
                              text="The station's bar is lively and well-furnished. A long counter runs along one wall, with shelves of drinks behind it. Tables and chairs are scattered about, and soft music plays in the background.",
                              font=("Arial", 12), bg="black", fg="white", wraplength=600)
        desc_label.pack(pady=10)
        
        # Room actions
        self.button_frame = tk.Frame(self.bar_window, bg="black")
        self.button_frame.pack(pady=20)
        
        # Check if user is a bartender or captain
        is_bartender = self.player_data.get("job") == "Bartender"
        is_captain = self.player_data.get("job") == "Captain"
        
        if is_bartender or is_captain:
            # Add bartender station access
            station_btn = tk.Button(self.button_frame, text="Enter Bartender Station", font=("Arial", 14), width=20, command=self.access_bartender_station)
            station_btn.pack(pady=10)
            
            # Add door lock/unlock button for bartenders and captains
            door_btn = tk.Button(self.button_frame, text="Lock/Unlock Door", font=("Arial", 14), width=20, command=self.toggle_door_lock)
            door_btn.pack(pady=10)
            
            # Add "Room Options" button to show regular options
            options_btn = tk.Button(self.button_frame, text="Room Options", font=("Arial", 14), width=20, command=self.show_room_options)
            options_btn.pack(pady=10)
        else:
            # Show regular options for non-bartenders
            self.show_room_options()
        
        # Exit button
        exit_btn = tk.Button(self.bar_window, text="Exit Room", font=("Arial", 14), width=15, command=self.on_closing)
        exit_btn.pack(pady=20)
    
    def show_room_options(self):
        """Show regular room options that all players can access"""
        # Clear existing buttons
        for widget in self.button_frame.winfo_children():
            widget.destroy()
            
        # Order drinks button
        order_btn = tk.Button(self.button_frame, text="Order Drinks", font=("Arial", 14), width=20, command=self.show_drink_menu)
        order_btn.pack(pady=10)
        
        # Socialize option
        socialize_btn = tk.Button(self.button_frame, text="Socialize", font=("Arial", 14), width=20, command=self.socialize)
        socialize_btn.pack(pady=10)
        
        # Only show "Back to Station Menu" if player is a bartender
        is_bartender = self.player_data.get("job") == "Bartender"
        if is_bartender:
            # Back to station menu button
            back_btn = tk.Button(self.button_frame, text="Back to Station Menu", font=("Arial", 14), width=20, 
                               command=self.show_station_menu)
            back_btn.pack(pady=10)
    
    def show_drink_menu(self):
        """Show the menu of available drinks"""
        # Create a popup for the drink menu
        menu_popup = tk.Toplevel(self.bar_window)
        menu_popup.title("Drink Menu")
        menu_popup.geometry("700x600")  # Made wider to accommodate tab buttons
        menu_popup.configure(bg="black")
        menu_popup.transient(self.bar_window)
        menu_popup.grab_set()
        
        # Center the popup
        menu_popup.update_idletasks()
        width = 700
        height = 600
        x = (menu_popup.winfo_screenwidth() // 2) - (width // 2)
        y = (menu_popup.winfo_screenheight() // 2) - (height // 2)
        menu_popup.geometry(f"{width}x{height}+{x}+{y}")
        
        # Title
        title_label = tk.Label(menu_popup, text="Drink Menu", font=("Arial", 18), bg="black", fg="white")
        title_label.pack(pady=10)
        
        # Current credits
        credits_label = tk.Label(menu_popup, text=f"Your credits: {self.player_data['credits']}", 
                             font=("Arial", 14), bg="black", fg="white")
        credits_label.pack(pady=5)
        
        # Create menu tabs for different categories
        tab_frame = tk.Frame(menu_popup, bg="black")
        tab_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # Create frame for the menu
        menu_frame = tk.Frame(menu_popup, bg="black")
        menu_frame.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)
        
        # Create scrollbar
        scrollbar = tk.Scrollbar(menu_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Create listbox for the drinks
        drink_listbox = tk.Listbox(menu_frame, bg="black", fg="white", font=("Arial", 12),
                                width=50, height=20, yscrollcommand=scrollbar.set)
        drink_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=drink_listbox.yview)
        
        # Description frame
        desc_frame = tk.Frame(menu_popup, bg="black")
        desc_frame.pack(padx=20, pady=5, fill=tk.X)
        
        # Create description label - moved before the function that uses it
        desc_label = tk.Label(desc_frame, text="Select a drink to see its description", 
                          font=("Arial", 12), bg="black", fg="white", wraplength=600)
        desc_label.pack()
        
        # Organize drinks into categories
        basic_drinks = {}
        mixed_drinks = {}
        all_drinks = {}
        
        # Copy the drinks to their respective categories
        for name, details in self.drinks_menu.items():
            basic_drinks[name] = details
            all_drinks[name] = details
            
        for name, details in self.mixed_drinks.items():
            mixed_drinks[name] = details
            all_drinks[name] = details
        
        # Track the current category and selected drink
        current_category = {"drinks": all_drinks, "name": "All Drinks"}
        selected_drink = {"name": "", "details": None}
        
        # Function to populate the listbox with a category
        def show_category(category_drinks, category_name):
            # Clear the listbox
            drink_listbox.delete(0, tk.END)
            
            # Update current category
            current_category["drinks"] = category_drinks
            current_category["name"] = category_name
            
            # Add header
            drink_listbox.insert(tk.END, f"--- {category_name} ---")
            
            # Add drinks to the listbox
            for drink, details in category_drinks.items():
                drink_listbox.insert(tk.END, f"{drink} - {details['price']} credits")
            
            # Reset the description
            desc_label.config(text="Select a drink to see its description")
        
        # Create the category buttons with more spacing
        all_btn = tk.Button(tab_frame, text="All Drinks", font=("Arial", 12), width=12,
                         command=lambda: show_category(all_drinks, "All Drinks"))
        all_btn.pack(side=tk.LEFT, padx=15)
        
        basic_btn = tk.Button(tab_frame, text="Basic Drinks", font=("Arial", 12), width=12,
                           command=lambda: show_category(basic_drinks, "Basic Drinks"))
        basic_btn.pack(side=tk.LEFT, padx=15)
        
        mixed_btn = tk.Button(tab_frame, text="Mixed Drinks", font=("Arial", 12), width=12,
                           command=lambda: show_category(mixed_drinks, "Mixed Drinks"))
        mixed_btn.pack(side=tk.LEFT, padx=15)
        
        # Show all drinks by default
        show_category(all_drinks, "All Drinks")
        
        # Update description when a drink is selected
        def on_select(event):
            selection = drink_listbox.curselection()
            if not selection or selection[0] == 0:  # Skip the header
                return
                
            # Get the selected drink name by parsing the listbox entry
            index = selection[0]
            entry = drink_listbox.get(index)
            
            # Parse the entry to get the drink name
            if " - " in entry:
                drink_name = entry.split(" - ")[0]
                
                # Find the drink details in the current category
                if drink_name in current_category["drinks"]:
                    drink_details = current_category["drinks"][drink_name]
                    desc_label.config(text=drink_details['desc'])
                    
                    # Update the selected drink
                    selected_drink["name"] = drink_name
                    selected_drink["details"] = drink_details
            
        drink_listbox.bind('<<ListboxSelect>>', on_select)
        
        # Buttons frame
        btn_frame = tk.Frame(menu_popup, bg="black")
        btn_frame.pack(pady=10)
        
        # Order button
        order_btn = tk.Button(btn_frame, text="Order Selected Drink", font=("Arial", 12), 
                           command=lambda: self.order_drink_from_menu(selected_drink, menu_popup, credits_label))
        order_btn.pack(side=tk.LEFT, padx=10)
        
        # Close button
        close_btn = tk.Button(btn_frame, text="Close Menu", font=("Arial", 12), command=menu_popup.destroy)
        close_btn.pack(side=tk.LEFT, padx=10)
    
    def order_drink_from_menu(self, selected_drink, popup, credits_label):
        """Process an order for a drink selected from the menu"""
        # Check if a drink is selected
        if not selected_drink["name"] or not selected_drink["details"]:
            tk.messagebox.showinfo("Selection Needed", "Please select a drink first", parent=popup)
            return
        
        drink_name = selected_drink["name"]
        drink_details = selected_drink["details"]
        
        # Check if player has enough credits
        if self.player_data['credits'] < drink_details['price']:
            tk.messagebox.showinfo("Insufficient Credits", 
                               f"You don't have enough credits to order {drink_name}.", 
                               parent=popup)
            return
        
        # Process the order
        self.player_data['credits'] -= drink_details['price']
        
        # Update the credits display
        credits_label.config(text=f"Your credits: {self.player_data['credits']}")
        
        # Add a note about the purchase
        if "notes" not in self.player_data:
            self.player_data["notes"] = []
        
        self.player_data["notes"].append({
            "timestamp": datetime.datetime.now().isoformat(),
            "text": f"Purchased {drink_name} at the bar for {drink_details['price']} credits."
        })
        
        # Show confirmation message
        tk.messagebox.showinfo("Order Successful", 
                           f"You've ordered a {drink_name} for {drink_details['price']} credits. Enjoy!", 
                           parent=popup)
    
    def socialize(self):
        """Interact with other crew members in the bar"""
        conversations = [
            "You chat with a group of engineers about the latest station upgrades.",
            "A security officer shares stories about past incidents on the station.",
            "You overhear some interesting gossip about the captain's leadership style.",
            "A doctor tells you about a strange medical case they recently handled.",
            "Several crew members are discussing the latest sports match from Earth.",
            "You find yourself in a philosophical debate about space exploration with a scientist."
        ]
        
        # Select a random conversation
        conversation = random.choice(conversations)
        
        # Show the conversation result
        self.bar_window.after(10, lambda: tk.messagebox.showinfo("Socializing", conversation, parent=self.bar_window))
        
        # Make sure the window stays on top after dialog
        self.bar_window.after(20, self.bar_window.lift)
        self.bar_window.focus_force()
    
    def access_bartender_station(self):
        """Access the bartender station for mixing drinks"""
        # Clear existing buttons
        for widget in self.button_frame.winfo_children():
            widget.destroy()
            
        # Set bartender mode
        self.bartender_mode = True
        
        # Add drink mixing button
        mix_btn = tk.Button(self.button_frame, text="Mix Drinks", font=("Arial", 14), width=20, command=self.show_drink_mixer)
        mix_btn.pack(pady=10)
        
        # Add button to view list of recipes
        recipes_btn = tk.Button(self.button_frame, text="View Recipes", font=("Arial", 14), width=20, command=self.show_recipes)
        recipes_btn.pack(pady=10)
        
        # Add button to serve premade drinks (same as regular menu)
        serve_btn = tk.Button(self.button_frame, text="Serve Regular Drinks", font=("Arial", 14), width=20, command=self.show_drink_menu)
        serve_btn.pack(pady=10)
        
        # Back button
        back_btn = tk.Button(self.button_frame, text="Back to Station Menu", font=("Arial", 14), width=20, 
                           command=self.show_station_menu)
        back_btn.pack(pady=10)
    
    def show_drink_mixer(self):
        """Show interface for mixing custom drinks"""
        # Create a popup for mixing drinks
        mixer_popup = tk.Toplevel(self.bar_window)
        mixer_popup.title("Bartender's Drink Mixer")
        mixer_popup.geometry("800x650")  # Made larger to accommodate all content
        mixer_popup.configure(bg="black")
        mixer_popup.transient(self.bar_window)
        mixer_popup.grab_set()
        
        # Center the popup
        mixer_popup.update_idletasks()
        width = 800
        height = 650
        x = (mixer_popup.winfo_screenwidth() // 2) - (width // 2)
        y = (mixer_popup.winfo_screenheight() // 2) - (height // 2)
        mixer_popup.geometry(f"{width}x{height}+{x}+{y}")
        
        # Create main canvas with scrollbar for the entire content
        main_canvas = tk.Canvas(mixer_popup, bg="black", highlightthickness=0)
        main_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Add scrollbar to the main canvas
        main_scrollbar = tk.Scrollbar(mixer_popup, orient=tk.VERTICAL, command=main_canvas.yview)
        main_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        main_canvas.configure(yscrollcommand=main_scrollbar.set)
        
        # Create a frame inside the canvas to hold all content
        content_frame = tk.Frame(main_canvas, bg="black")
        content_frame.bind("<Configure>", lambda e: main_canvas.configure(scrollregion=main_canvas.bbox("all")))
        main_canvas.create_window((0, 0), window=content_frame, anchor=tk.NW)
        
        # Title
        title_label = tk.Label(content_frame, text="Bartender's Drink Mixer", font=("Arial", 18), bg="black", fg="white")
        title_label.pack(pady=10)
        
        # Main frame containing left and right sections
        main_frame = tk.Frame(content_frame, bg="black")
        main_frame.pack(pady=10, fill=tk.BOTH, expand=True)
        
        # Left section: Ingredient selection
        left_frame = tk.Frame(main_frame, bg="black", width=375)
        left_frame.pack(side=tk.LEFT, padx=10, fill=tk.BOTH, expand=True)
        
        # Ingredient category frame
        category_frame = tk.Frame(left_frame, bg="black")
        category_frame.pack(fill=tk.X, pady=5)
        
        category_label = tk.Label(category_frame, text="Ingredient Categories:", font=("Arial", 14), bg="black", fg="white")
        category_label.pack(anchor=tk.W, pady=5)
        
        # Ingredient category buttons
        btn_frame = tk.Frame(category_frame, bg="black")
        btn_frame.pack(fill=tk.X)
        
        # Group ingredients by category
        spirits = [i for i in self.available_ingredients if i in ["Vodka", "Gin", "Rum", "Whiskey", "Tequila", "Brandy", "Scotch"]]
        mixers = [i for i in self.available_ingredients if "Juice" in i or "Water" in i or "Cola" in i or "Ale" in i or "Sprite" in i]
        modifiers = [i for i in self.available_ingredients if i in ["Lemon Juice", "Lime Juice", "Sugar", "Salt", "Honey", "Triple Sec", 
                                                            "Blue Curacao", "Orange Curacao", "Grenadine", "Bitters", "Vermouth", 
                                                            "Campari", "Cherry Brandy"]]
        specials = [i for i in self.available_ingredients if i not in spirits and i not in mixers and i not in modifiers]

        # Current category tracker
        current_category = {"items": self.available_ingredients}

        # Available ingredients frame with scrollbar
        ing_frame = tk.LabelFrame(left_frame, text="Available Ingredients", font=("Arial", 12), bg="black", fg="white")
        ing_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Scrollbar for ingredients
        ing_scrollbar = tk.Scrollbar(ing_frame)
        ing_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Listbox for ingredients
        ing_listbox = tk.Listbox(ing_frame, bg="black", fg="white", font=("Arial", 12),
                              width=20, height=12, yscrollcommand=ing_scrollbar.set)
        ing_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        ing_scrollbar.config(command=ing_listbox.yview)
        
        # Function to update the ingredients listbox based on category
        def show_category(items, category_name):
            # Clear the listbox
            ing_listbox.delete(0, tk.END)
            
            # Update current category
            current_category["items"] = items
            
            # Add header
            ing_listbox.insert(tk.END, f"--- {category_name} ---")
            
            # Add sorted ingredients to the listbox
            for item in sorted(items):
                ing_listbox.insert(tk.END, item)
        
        # Create category buttons
        all_btn = tk.Button(btn_frame, text="All", font=("Arial", 10), 
                         command=lambda: show_category(self.available_ingredients, "All Ingredients"))
        all_btn.pack(side=tk.LEFT, padx=5, pady=5)
        
        spirits_btn = tk.Button(btn_frame, text="Spirits", font=("Arial", 10), 
                             command=lambda: show_category(spirits, "Spirits"))
        spirits_btn.pack(side=tk.LEFT, padx=5, pady=5)
        
        mixers_btn = tk.Button(btn_frame, text="Mixers", font=("Arial", 10), 
                            command=lambda: show_category(mixers, "Mixers"))
        mixers_btn.pack(side=tk.LEFT, padx=5, pady=5)
        
        modifiers_btn = tk.Button(btn_frame, text="Modifiers", font=("Arial", 10), 
                               command=lambda: show_category(modifiers, "Modifiers"))
        modifiers_btn.pack(side=tk.LEFT, padx=5, pady=5)
        
        specials_btn = tk.Button(btn_frame, text="Specials", font=("Arial", 10), 
                              command=lambda: show_category(specials, "Special Ingredients"))
        specials_btn.pack(side=tk.LEFT, padx=5, pady=5)
        
        # Show all ingredients by default
        show_category(self.available_ingredients, "All Ingredients")
        
        # Add ingredient button
        add_btn = tk.Button(left_frame, text="Add Ingredient →", font=("Arial", 12), 
                         command=lambda: self.add_to_mix(ing_listbox, mix_listbox, current_category["items"]))
        add_btn.pack(pady=10)
        
        # Right section: Mixing glass and results
        right_frame = tk.Frame(main_frame, bg="black", width=375)
        right_frame.pack(side=tk.RIGHT, padx=10, fill=tk.BOTH, expand=True)
        
        # Mixing glass frame with scrollbar
        mix_frame = tk.LabelFrame(right_frame, text="Mixing Glass", font=("Arial", 12), bg="black", fg="white")
        mix_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Scrollbar for mixing glass
        mix_scrollbar = tk.Scrollbar(mix_frame)
        mix_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Listbox for mixing glass ingredients
        mix_listbox = tk.Listbox(mix_frame, bg="black", fg="white", font=("Arial", 12),
                              width=20, height=12, yscrollcommand=mix_scrollbar.set)
        mix_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        mix_scrollbar.config(command=mix_listbox.yview)
        
        # Button to remove ingredient
        remove_btn = tk.Button(right_frame, text="← Remove Ingredient", font=("Arial", 12), 
                            command=lambda: self.remove_from_mix(mix_listbox))
        remove_btn.pack(pady=5)
        
        # Clear glass button
        clear_btn = tk.Button(right_frame, text="Clear Glass", font=("Arial", 12), 
                           command=lambda: mix_listbox.delete(0, tk.END))
        clear_btn.pack(pady=5)
        
        # Result frame
        result_frame = tk.LabelFrame(content_frame, text="Mixing Result", font=("Arial", 12), bg="black", fg="white")
        result_frame.pack(padx=20, pady=10, fill=tk.X)
        
        # Result label
        result_label = tk.Label(result_frame, text="Mix ingredients to create a drink", 
                            font=("Arial", 12), bg="black", fg="white", wraplength=700)
        result_label.pack(pady=10, fill=tk.X)
        
        # Bottom buttons frame
        bottom_frame = tk.Frame(content_frame, bg="black")
        bottom_frame.pack(pady=10)
        
        # Mix button
        mix_btn = tk.Button(bottom_frame, text="Mix Drink", font=("Arial", 14), bg="dark blue", fg="white",
                         command=lambda: self.mix_drink(mix_listbox, result_label))
        mix_btn.pack(side=tk.LEFT, padx=20)
        
        # Recipe reference button
        recipe_btn = tk.Button(bottom_frame, text="Recipe Book", font=("Arial", 14),
                            command=self.show_recipes)
        recipe_btn.pack(side=tk.LEFT, padx=20)
        
        # Close button
        close_btn = tk.Button(bottom_frame, text="Close", font=("Arial", 14), 
                           command=mixer_popup.destroy)
        close_btn.pack(side=tk.LEFT, padx=20)

        # Function to handle mousewheel scrolling
        def _on_mousewheel(event):
            main_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        # Bind mousewheel to the mixer popup window
        mixer_popup.bind("<MouseWheel>", _on_mousewheel)
        
        # Override the destroy method to unbind the mousewheel event
        orig_destroy = mixer_popup.destroy
        def _destroy_and_cleanup():
            mixer_popup.unbind("<MouseWheel>")
            orig_destroy()
        
        mixer_popup.destroy = _destroy_and_cleanup
        
        # Configure the window close action to call our custom destroy method
        mixer_popup.protocol("WM_DELETE_WINDOW", mixer_popup.destroy)
    
    def add_to_mix(self, ing_listbox, mix_listbox, available_items):
        """Add an ingredient to the mixing glass"""
        selection = ing_listbox.curselection()
        if not selection or selection[0] == 0:  # Skip header
            return
        
        index = selection[0]
        entry = ing_listbox.get(index)
        
        # Skip if it's a category header
        if entry.startswith("---"):
            return
            
        # Add to mixing glass
        mix_listbox.insert(tk.END, entry)
    
    def mix_drink(self, mix_listbox, result_label):
        """Mix ingredients and determine the result"""
        # Get all ingredients from the mixing glass
        ingredients = [mix_listbox.get(i) for i in range(mix_listbox.size())]
        
        if not ingredients:
            result_label.config(text="You need to add ingredients first!")
            return
        
        # Sort ingredients for consistent matching
        ingredients.sort()
        
        # Check if the mix matches any known recipes
        drink_match = None
        for drink_name, drink_data in self.mixed_drinks.items():
            recipe_ingredients = sorted(drink_data["ingredients"])
            if ingredients == recipe_ingredients:
                drink_match = drink_name
                break
        
        if drink_match:
            # Successfully mixed a known drink
            drink_data = self.mixed_drinks[drink_match]
            result_text = f"Success! You've mixed a {drink_match}.\n{drink_data['desc']}"
            result_label.config(text=result_text, fg="light green")
            
            # Add note about the successful mix
            if "notes" not in self.player_data:
                self.player_data["notes"] = []
            
            self.player_data["notes"].append({
                "timestamp": datetime.datetime.now().isoformat(),
                "text": f"Successfully mixed a {drink_match} at the bar."
            })
        else:
            # Define spirits for feedback
            spirits = ["Vodka", "Gin", "Rum", "Whiskey", "Tequila", "Brandy", "Scotch"]
            
            # Analyze the mix to give feedback
            if len(ingredients) > 5:
                feedback = "This has too many ingredients - most cocktails use 2-5 ingredients."
            elif not any(item in spirits for item in ingredients):
                feedback = "Most mixed drinks need a spirit as the base (like Vodka, Rum, or Whiskey)."
            elif all(item in spirits for item in ingredients):
                feedback = "This is just a mix of different spirits. Try adding some mixers or modifiers."
            else:
                feedback = "This combination doesn't match any known recipe. Try a different mix."
                
            # Unknown mixture
            result_text = f"You've created an unknown concoction. {feedback}"
            result_label.config(text=result_text, fg="red")
    
    def show_recipes(self):
        """Show a list of known drink recipes"""
        recipes_popup = tk.Toplevel(self.bar_window)
        recipes_popup.title("Drink Recipes")
        recipes_popup.geometry("700x600")  # Made larger for more recipes
        recipes_popup.configure(bg="black")
        recipes_popup.transient(self.bar_window)
        recipes_popup.grab_set()
        
        # Center the popup
        recipes_popup.update_idletasks()
        width = 700
        height = 600
        x = (recipes_popup.winfo_screenwidth() // 2) - (width // 2)
        y = (recipes_popup.winfo_screenheight() // 2) - (height // 2)
        recipes_popup.geometry(f"{width}x{height}+{x}+{y}")
        
        # Title
        title_label = tk.Label(recipes_popup, text="Bartender's Recipe Book", font=("Arial", 18), bg="black", fg="white")
        title_label.pack(pady=10)
        
        # Recipe navigation frame
        nav_frame = tk.Frame(recipes_popup, bg="black")
        nav_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Recipe category buttons
        all_btn = tk.Button(nav_frame, text="All Recipes", font=("Arial", 10),
                         command=lambda: show_recipe_category("all"))
        all_btn.pack(side=tk.LEFT, padx=5)
        
        basic_btn = tk.Button(nav_frame, text="Basic Recipes", font=("Arial", 10),
                           command=lambda: show_recipe_category("basic"))
        basic_btn.pack(side=tk.LEFT, padx=5)
        
        advanced_btn = tk.Button(nav_frame, text="Advanced Recipes", font=("Arial", 10),
                          command=lambda: show_recipe_category("advanced"))
        advanced_btn.pack(side=tk.LEFT, padx=5)
        
        special_btn = tk.Button(nav_frame, text="Station Specials", font=("Arial", 10),
                         command=lambda: show_recipe_category("special"))
        special_btn.pack(side=tk.LEFT, padx=5)
        
        # Recipe categories
        basic_recipes = ["Screwdriver", "Gin and Tonic", "Rum and Cola", "Whiskey Sour", "Daiquiri"]
        special_recipes = ["Space Blaster", "Quantum Fizz", "Nebula Cloud"]
        
        # Create scrollable frame for recipes
        frame = tk.Frame(recipes_popup, bg="black")
        frame.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)
        
        # Add scrollbar
        scrollbar = tk.Scrollbar(frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Create text widget for recipes
        recipe_text = tk.Text(frame, bg="black", fg="white", font=("Arial", 12),
                           width=60, height=25, yscrollcommand=scrollbar.set, wrap=tk.WORD)
        recipe_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=recipe_text.yview)
        
        # Mouse wheel binding for scrolling
        def _on_recipe_mousewheel(event):
            try:
                recipe_text.yview_scroll(int(-1*(event.delta/120)), "units")
            except tk.TclError:
                pass  # Ignore errors if the text widget was destroyed
        
        # Bind mousewheel to recipe text
        recipes_popup.bind("<MouseWheel>", _on_recipe_mousewheel)
        
        # Override destroy method to cleanup bindings
        orig_destroy = recipes_popup.destroy
        def _destroy_and_cleanup():
            try:
                recipes_popup.unbind("<MouseWheel>")
            except:
                pass
            orig_destroy()
        
        recipes_popup.destroy = _destroy_and_cleanup
        
        # Format and display recipes by category
        def show_recipe_category(category):
            # Clear the text widget
            recipe_text.config(state=tk.NORMAL)
            recipe_text.delete(1.0, tk.END)
            
            # Add a header
            recipe_text.insert(tk.END, "BARTENDER'S RECIPE BOOK\n", "header")
            recipe_text.insert(tk.END, "------------------------\n\n", "header")
            
            # Create a sorted list of drink names
            sorted_drinks = sorted(self.mixed_drinks.keys())
            
            # Filter by category if needed
            if category == "basic":
                sorted_drinks = [drink for drink in sorted_drinks if drink in basic_recipes]
                recipe_text.insert(tk.END, "BASIC COCKTAILS\n\n", "category")
            elif category == "special":
                sorted_drinks = [drink for drink in sorted_drinks if drink in special_recipes]
                recipe_text.insert(tk.END, "STATION SPECIALTIES\n\n", "category")
            elif category == "advanced":
                sorted_drinks = [drink for drink in sorted_drinks if drink not in basic_recipes and drink not in special_recipes]
                recipe_text.insert(tk.END, "ADVANCED COCKTAILS\n\n", "category")
            else:
                # Add all categories with headers
                recipe_text.insert(tk.END, "BASIC COCKTAILS\n\n", "category")
                for drink in sorted(basic_recipes):
                    add_recipe(drink)
                
                recipe_text.insert(tk.END, "\nADVANCED COCKTAILS\n\n", "category")
                for drink in sorted([d for d in sorted_drinks if d not in basic_recipes and d not in special_recipes]):
                    add_recipe(drink)
                
                recipe_text.insert(tk.END, "\nSTATION SPECIALTIES\n\n", "category")
                for drink in sorted(special_recipes):
                    add_recipe(drink)
                
                # Make text widget read-only
                recipe_text.config(state=tk.DISABLED)
                return
            
            # Add recipes for the selected category
            for drink in sorted_drinks:
                add_recipe(drink)
            
            # Make text widget read-only
            recipe_text.config(state=tk.DISABLED)
        
        # Helper function to add a recipe
        def add_recipe(drink_name):
            if drink_name in self.mixed_drinks:
                drink_data = self.mixed_drinks[drink_name]
                
                # Add drink name
                recipe_text.insert(tk.END, f"{drink_name}:\n", "drink_name")
                
                # Add ingredients
                recipe_text.insert(tk.END, f"  Ingredients: ", "label")
                recipe_text.insert(tk.END, f"{', '.join(drink_data['ingredients'])}\n", "ingredients")
                
                # Add price
                recipe_text.insert(tk.END, f"  Price: ", "label")
                recipe_text.insert(tk.END, f"{drink_data['price']} credits\n", "value")
                
                # Add description
                recipe_text.insert(tk.END, f"  Description: ", "label")
                recipe_text.insert(tk.END, f"{drink_data['desc']}\n\n", "value")
        
        # Configure text tags for formatting
        recipe_text.tag_configure("header", font=("Arial", 14, "bold"))
        recipe_text.tag_configure("category", font=("Arial", 13, "bold"), foreground="yellow")
        recipe_text.tag_configure("drink_name", font=("Arial", 12, "bold"), foreground="light blue")
        recipe_text.tag_configure("label", font=("Arial", 11, "bold"))
        recipe_text.tag_configure("ingredients", font=("Arial", 11), foreground="light green")
        recipe_text.tag_configure("value", font=("Arial", 11))
        
        # Show all recipes by default
        show_recipe_category("all")
        
        # Search frame
        search_frame = tk.Frame(recipes_popup, bg="black")
        search_frame.pack(fill=tk.X, padx=20, pady=5)
        
        search_label = tk.Label(search_frame, text="Search: ", font=("Arial", 11), bg="black", fg="white")
        search_label.pack(side=tk.LEFT, padx=5)
        
        search_entry = tk.Entry(search_frame, bg="dark gray", fg="white", font=("Arial", 11), width=20)
        search_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        # Function to search recipes
        def search_recipes(event=None):
            query = search_entry.get().lower().strip()
            if not query:
                show_recipe_category("all")
                return
                
            # Clear the text widget
            recipe_text.config(state=tk.NORMAL)
            recipe_text.delete(1.0, tk.END)
            
            # Add a header
            recipe_text.insert(tk.END, f"SEARCH RESULTS FOR '{query}'\n", "header")
            recipe_text.insert(tk.END, "------------------------\n\n", "header")
            
            # Search through drinks and ingredients
            results_found = False
            for drink_name, drink_data in self.mixed_drinks.items():
                # Check if query matches drink name or ingredients
                if (query in drink_name.lower() or 
                    any(query in ingredient.lower() for ingredient in drink_data["ingredients"]) or
                    query in drink_data["desc"].lower()):
                    add_recipe(drink_name)
                    results_found = True
            
            if not results_found:
                recipe_text.insert(tk.END, "No recipes found matching your search.")
                
            # Make text widget read-only
            recipe_text.config(state=tk.DISABLED)
        
        # Bind search function to entry
        search_entry.bind("<Return>", search_recipes)
        
        search_btn = tk.Button(search_frame, text="Search", font=("Arial", 10), command=search_recipes)
        search_btn.pack(side=tk.LEFT, padx=5)
        
        # Ingredient list button
        ing_btn = tk.Button(search_frame, text="Ingredients List", font=("Arial", 10),
                         command=self.show_ingredients_list)
        ing_btn.pack(side=tk.LEFT, padx=5)
        
        # Close button
        close_btn = tk.Button(recipes_popup, text="Close", font=("Arial", 12), command=recipes_popup.destroy)
        close_btn.pack(pady=10)
    
    def show_ingredients_list(self):
        """Show a list of all available ingredients"""
        ing_popup = tk.Toplevel(self.bar_window)
        ing_popup.title("Available Ingredients")
        ing_popup.geometry("400x500")
        ing_popup.configure(bg="black")
        ing_popup.transient(self.bar_window)
        ing_popup.grab_set()
        
        # Center the popup
        ing_popup.update_idletasks()
        width = 400
        height = 500
        x = (ing_popup.winfo_screenwidth() // 2) - (width // 2)
        y = (ing_popup.winfo_screenheight() // 2) - (height // 2)
        ing_popup.geometry(f"{width}x{height}+{x}+{y}")
        
        # Title
        title_label = tk.Label(ing_popup, text="Available Ingredients", font=("Arial", 18), bg="black", fg="white")
        title_label.pack(pady=10)
        
        # Group ingredients by category
        spirits = []
        mixers = []
        modifiers = []
        specials = []
        
        # Organize ingredients into categories
        for ingredient in sorted(self.available_ingredients):
            if ingredient in ["Vodka", "Gin", "Rum", "Whiskey", "Tequila", "Brandy", "Scotch"]:
                spirits.append(ingredient)
            elif "Juice" in ingredient or "Water" in ingredient or "Cola" in ingredient or "Ale" in ingredient or "Sprite" in ingredient:
                mixers.append(ingredient)
            elif ingredient in ["Lemon Juice", "Lime Juice", "Sugar", "Salt", "Honey", "Triple Sec", 
                              "Blue Curacao", "Orange Curacao", "Grenadine", "Bitters", "Vermouth", 
                              "Campari", "Cherry Brandy"]:
                modifiers.append(ingredient)
            else:
                specials.append(ingredient)
        
        # Create scrollable frame for ingredients
        frame = tk.Frame(ing_popup, bg="black")
        frame.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)
        
        # Add scrollbar
        scrollbar = tk.Scrollbar(frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Create text widget for ingredients
        ing_text = tk.Text(frame, bg="black", fg="white", font=("Arial", 12),
                        width=40, height=20, yscrollcommand=scrollbar.set, wrap=tk.WORD)
        ing_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=ing_text.yview)
        
        # Mouse wheel binding for scrolling
        def _on_ing_mousewheel(event):
            try:
                ing_text.yview_scroll(int(-1*(event.delta/120)), "units")
            except tk.TclError:
                pass  # Ignore errors if the text widget was destroyed
        
        # Bind mousewheel to ingredients text
        ing_popup.bind("<MouseWheel>", _on_ing_mousewheel)
        
        # Override destroy method to cleanup bindings
        orig_destroy = ing_popup.destroy
        def _destroy_and_cleanup():
            try:
                ing_popup.unbind("<MouseWheel>")
            except:
                pass
            orig_destroy()
        
        ing_popup.destroy = _destroy_and_cleanup
        
        # Add ingredients by category
        ing_text.insert(tk.END, "SPIRITS\n", "header")
        ing_text.insert(tk.END, "-------\n", "header")
        for ingredient in spirits:
            ing_text.insert(tk.END, f"• {ingredient}\n", "ingredient")
        
        ing_text.insert(tk.END, "\nMIXERS\n", "header")
        ing_text.insert(tk.END, "------\n", "header")
        for ingredient in mixers:
            ing_text.insert(tk.END, f"• {ingredient}\n", "ingredient")
        
        ing_text.insert(tk.END, "\nMODIFIERS\n", "header")
        ing_text.insert(tk.END, "---------\n", "header")
        for ingredient in modifiers:
            ing_text.insert(tk.END, f"• {ingredient}\n", "ingredient")
        
        ing_text.insert(tk.END, "\nSPECIAL INGREDIENTS\n", "header")
        ing_text.insert(tk.END, "------------------\n", "header")
        for ingredient in specials:
            ing_text.insert(tk.END, f"• {ingredient}\n", "ingredient")
        
        # Configure text tags for formatting
        ing_text.tag_configure("header", font=("Arial", 14, "bold"))
        ing_text.tag_configure("ingredient", font=("Arial", 11))
        
        # Make text widget read-only
        ing_text.config(state=tk.DISABLED)
        
        # Close button
        close_btn = tk.Button(ing_popup, text="Close", font=("Arial", 12), command=ing_popup.destroy)
        close_btn.pack(pady=10)
    
    def toggle_door_lock(self):
        """Toggle the lock on the bar door"""
        # Get the door location key
        door_key = "0,-1"  # Bar door
        
        # Get the ship map from player data
        if "ship_map" not in self.player_data:
            self.bar_window.after(10, lambda: tk.messagebox.showinfo("Door Control", 
                                                             "Unable to access door control system.", 
                                                             parent=self.bar_window))
            return
            
        ship_map = self.player_data["ship_map"]
        if door_key not in ship_map:
            self.bar_window.after(10, lambda: tk.messagebox.showinfo("Door Control", 
                                                             "Unable to access door control system.", 
                                                             parent=self.bar_window))
            return
            
        # Toggle the door lock
        if ship_map[door_key].get("locked", False):
            ship_map[door_key]["locked"] = False
            ship_map[door_key]["desc"] = "The station's social hub where crew members can relax and enjoy drinks. The door is unlocked."
            self.bar_window.after(10, lambda: tk.messagebox.showinfo("Door Control", 
                                                             "The Bar door has been unlocked.", 
                                                             parent=self.bar_window))
        else:
            ship_map[door_key]["locked"] = True
            ship_map[door_key]["desc"] = "The station's social hub where crew members can relax and enjoy drinks. The door is locked."
            self.bar_window.after(10, lambda: tk.messagebox.showinfo("Door Control", 
                                                             "The Bar door has been locked.", 
                                                             parent=self.bar_window))
        
        # Update ship map in player data
        self.player_data["ship_map"] = ship_map
        
        # Make sure the window stays on top after dialog
        self.bar_window.after(20, self.bar_window.lift)
        self.bar_window.focus_force()
    
    def on_closing(self):
        """Handle window closing"""
        # Check if the door is locked
        door_key = "0,-1"  # Bar door
        if self.player_data.get("ship_map", {}).get(door_key, {}).get("locked", False):
            self.bar_window.after(10, lambda: tk.messagebox.showinfo("Locked Door", "The door is locked. You must unlock it before leaving.", parent=self.bar_window))
            # Make sure the window stays on top after dialog
            self.bar_window.after(20, self.bar_window.lift)
            self.bar_window.focus_force()
            return
        
        # Reset bartender mode
        self.bartender_mode = False
        
        # Release grab before closing
        self.bar_window.grab_release()
        
        # Call return callback with player data
        self.return_callback(self.player_data)
        
        # Destroy the window
        self.bar_window.destroy()

    def show_station_menu(self):
        """Return to main station menu options"""
        # Reset bartender mode
        self.bartender_mode = False
        
        # Clear existing buttons
        for widget in self.button_frame.winfo_children():
            widget.destroy()
            
        # Check if user is a bartender or captain
        is_bartender = self.player_data.get("job") == "Bartender"
        is_captain = self.player_data.get("job") == "Captain"
        
        if is_bartender or is_captain:
            # Add bartender station access
            station_btn = tk.Button(self.button_frame, text="Enter Bartender Station", font=("Arial", 14), width=20, command=self.access_bartender_station)
            station_btn.pack(pady=10)
            
            # Add door lock/unlock button for bartenders and captains
            door_btn = tk.Button(self.button_frame, text="Lock/Unlock Door", font=("Arial", 14), width=20, command=self.toggle_door_lock)
            door_btn.pack(pady=10)
            
            # Add "Room Options" button to show regular options
            options_btn = tk.Button(self.button_frame, text="Room Options", font=("Arial", 14), width=20, command=self.show_room_options)
            options_btn.pack(pady=10)
        else:
            # Show regular options for unauthorized personnel
            self.show_room_options() 

    def remove_from_mix(self, mix_listbox):
        """Remove an ingredient from the mixing glass"""
        selection = mix_listbox.curselection()
        if not selection:
            return
        
        index = selection[0]
        mix_listbox.delete(index)

class Botany:
    def __init__(self, parent_window, player_data, return_callback):
        # Create a new toplevel window
        self.botany_window = tk.Toplevel(parent_window)
        self.botany_window.title("Botany Lab")
        self.botany_window.geometry("800x600")
        self.botany_window.configure(bg="black")
        
        # Store references
        self.parent_window = parent_window
        self.player_data = player_data
        self.return_callback = return_callback
        
        # Initialize botany data if it doesn't exist
        if "botany" not in self.player_data:
            self.player_data["botany"] = {
                "planters": [
                    {"occupied": False, "plant": None, "growth_stage": 0},
                    {"occupied": False, "plant": None, "growth_stage": 0},
                    {"occupied": False, "plant": None, "growth_stage": 0},
                    {"occupied": False, "plant": None, "growth_stage": 0}
                ],
                "seeds": []
            }
        
        # Available seeds in the seed machine
        self.available_seeds = [
            {"name": "Tomato Seeds", "description": "Grows into juicy red tomatoes."},
            {"name": "Potato Seeds", "description": "Produces starchy potatoes."},
            {"name": "Wheat Seeds", "description": "Grows into tall wheat stalks."},
            {"name": "Carrot Seeds", "description": "Produces orange root vegetables."},
            {"name": "Apple Seeds", "description": "Grows into small apple trees."}
        ]
        
        # Bind window closing
        self.botany_window.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Ensure this window stays on top
        self.botany_window.transient(parent_window)
        self.botany_window.grab_set()
        self.botany_window.focus_force()
        
        # Center window on screen after window is configured
        self.botany_window.update_idletasks()
        width = 800
        height = 600
        x = (self.botany_window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.botany_window.winfo_screenheight() // 2) - (height // 2)
        self.botany_window.geometry(f"{width}x{height}+{x}+{y}")
        
        # Title
        room_label = tk.Label(self.botany_window, text="Station Botany Lab", font=("Arial", 24), bg="black", fg="white")
        room_label.pack(pady=30)
        
        # Description
        desc_label = tk.Label(self.botany_window, 
                              text="The botany lab is filled with plants of all varieties. Hydroponic systems line the walls, and bright grow lights illuminate rows of planters. The air is humid and smells of fresh soil and vegetation.",
                              font=("Arial", 12), bg="black", fg="white", wraplength=600)
        desc_label.pack(pady=10)
        
        # Room actions
        self.button_frame = tk.Frame(self.botany_window, bg="black")
        self.button_frame.pack(pady=20)
        
        # Check if user has special access
        is_botanist = self.player_data.get("job") == "Botanist"
        is_captain = self.player_data.get("job") == "Captain"
        is_hop = self.player_data.get("job") == "Head of Personnel"
        has_botany_access = is_botanist or is_captain or is_hop or ("permissions" in self.player_data and self.player_data["permissions"].get("botany_station", False))
        
        if has_botany_access:
            # Show station access button for authorized personnel
            station_btn = tk.Button(self.button_frame, text="Enter Botany Station", font=("Arial", 14), width=20, command=self.access_botany_station)
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
        exit_btn = tk.Button(self.botany_window, text="Exit Room", font=("Arial", 14), width=15, command=self.on_closing)
        exit_btn.pack(pady=20)
    
    def show_room_options(self):
        """Show regular room options that all players can access"""
        # Clear existing buttons
        for widget in self.button_frame.winfo_children():
            widget.destroy()
            
        # View plants option
        view_plants_btn = tk.Button(self.button_frame, text="View Plants", font=("Arial", 14), width=20, command=self.view_plants)
        view_plants_btn.pack(pady=10)
        
        # Only show "Back to Station Menu" if player has access
        is_botanist = self.player_data.get("job") == "Botanist"
        is_captain = self.player_data.get("job") == "Captain"
        is_hop = self.player_data.get("job") == "Head of Personnel"
        has_botany_access = is_botanist or is_captain or is_hop or ("permissions" in self.player_data and self.player_data["permissions"].get("botany_station", False))
        
        if has_botany_access:
            # Back to station menu button
            back_btn = tk.Button(self.button_frame, text="Back to Station Menu", font=("Arial", 14), width=20, 
                               command=self.show_station_menu)
            back_btn.pack(pady=10)
    
    def view_plants(self):
        """View the plants in the botany lab"""
        # Create a new top-level window for viewing plants
        plants_window = tk.Toplevel(self.botany_window)
        plants_window.title("Viewing Plants")
        plants_window.geometry("600x500")
        plants_window.configure(bg="black")
        plants_window.transient(self.botany_window)
        plants_window.grab_set()
        
        # Center the window
        plants_window.update_idletasks()
        width = 600
        height = 500
        x = (plants_window.winfo_screenwidth() // 2) - (width // 2)
        y = (plants_window.winfo_screenheight() // 2) - (height // 2)
        plants_window.geometry(f"{width}x{height}+{x}+{y}")
        
        # Title
        title_label = tk.Label(plants_window, text="Botany Lab Plants", font=("Arial", 18, "bold"), bg="black", fg="white")
        title_label.pack(pady=15)
        
        # Description
        desc_text = "You observe the various plants growing in the hydroponic planters."
        desc_label = tk.Label(plants_window, text=desc_text, font=("Arial", 12), bg="black", fg="white", wraplength=500)
        desc_label.pack(pady=10)
        
        # Create a frame for the planters
        planters_frame = tk.Frame(plants_window, bg="black")
        planters_frame.pack(pady=20, fill=tk.BOTH, expand=True)
        
        # Show the current state of each planter
        planters = self.player_data["botany"]["planters"]
        for i, planter in enumerate(planters):
            planter_frame = tk.Frame(planters_frame, bg="#222222", bd=2, relief=tk.RIDGE, width=500)
            planter_frame.pack(fill=tk.X, padx=20, pady=5)
            
            if planter["occupied"]:
                plant_name = planter["plant"]
                growth_stage = planter["growth_stage"]
                growth_text = "Seedling" if growth_stage < 3 else "Growing" if growth_stage < 6 else "Mature"
                
                # Plant name
                name_label = tk.Label(planter_frame, text=f"Planter {i+1}: {plant_name}", 
                                    font=("Arial", 14, "bold"), bg="#222222", fg="light green")
                name_label.pack(anchor="w", padx=10, pady=5)
                
                # Plant stage
                stage_label = tk.Label(planter_frame, text=f"Stage: {growth_text} ({growth_stage}/10)", 
                                     font=("Arial", 12), bg="#222222", fg="white")
                stage_label.pack(anchor="w", padx=10, pady=5)
            else:
                # Empty planter
                name_label = tk.Label(planter_frame, text=f"Planter {i+1}: Empty", 
                                    font=("Arial", 14, "bold"), bg="#222222", fg="white")
                name_label.pack(anchor="w", padx=10, pady=5)
                
                # Description
                empty_label = tk.Label(planter_frame, text="This planter is ready for seeds.", 
                                    font=("Arial", 12), bg="#222222", fg="white")
                empty_label.pack(anchor="w", padx=10, pady=5)
        
        # Close button
        close_btn = tk.Button(plants_window, text="Close", font=("Arial", 14), width=15, command=plants_window.destroy)
        close_btn.pack(pady=20)
    
    def access_botany_station(self):
        """Access the botany station for authorized personnel"""
        # Show access confirmation for authorized personnel
        self.botany_window.after(10, lambda: messagebox.showinfo("Botany Station", "Access granted. Welcome to the Botany Station.", parent=self.botany_window))
        
        # Clear existing buttons
        for widget in self.button_frame.winfo_children():
            widget.destroy()
            
        # Title for the station
        station_label = tk.Label(self.button_frame, text="Botany Station Controls", font=("Arial", 16, "bold"), bg="black", fg="white")
        station_label.pack(pady=10)
        
        # Get seeds button
        seeds_btn = tk.Button(self.button_frame, text="Seed Machine", font=("Arial", 14), width=20, command=self.access_seed_machine)
        seeds_btn.pack(pady=10)
        
        # View plants button
        view_btn = tk.Button(self.button_frame, text="View Plants", font=("Arial", 14), width=20, command=self.view_plants)
        view_btn.pack(pady=10)
        
        # Plant seeds button
        plant_btn = tk.Button(self.button_frame, text="Plant Seeds", font=("Arial", 14), width=20, command=self.plant_seeds)
        plant_btn.pack(pady=10)
        
        # Back button
        back_btn = tk.Button(self.button_frame, text="Back to Main Menu", font=("Arial", 14), width=20, command=self.show_station_menu)
        back_btn.pack(pady=15)
        
        # Make sure the window stays on top after dialog
        self.botany_window.after(20, self.botany_window.lift)
        self.botany_window.focus_force()
    
    def access_seed_machine(self):
        """Access the seed machine to get seeds"""
        # Create a new toplevel window for the seed machine
        seed_window = tk.Toplevel(self.botany_window)
        seed_window.title("Seed Machine")
        seed_window.geometry("700x600")
        seed_window.configure(bg="black")
        seed_window.transient(self.botany_window)
        seed_window.grab_set()
        
        # Center the window
        seed_window.update_idletasks()
        width = 700
        height = 600
        x = (seed_window.winfo_screenwidth() // 2) - (width // 2)
        y = (seed_window.winfo_screenheight() // 2) - (height // 2)
        seed_window.geometry(f"{width}x{height}+{x}+{y}")
        
        # Title
        title_label = tk.Label(seed_window, text="Botanical Seed Dispenser", font=("Arial", 18, "bold"), bg="black", fg="white")
        title_label.pack(pady=15)
        
        # Description
        desc_text = "This machine dispenses seeds for cultivation in the botany lab's planters."
        desc_label = tk.Label(seed_window, text=desc_text, font=("Arial", 12), bg="black", fg="white", wraplength=600)
        desc_label.pack(pady=10)
        
        # Main frame to contain both left and right sides
        main_frame = tk.Frame(seed_window, bg="black")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left frame for available seeds
        left_frame = tk.LabelFrame(main_frame, text="Available Seeds", font=("Arial", 14), bg="black", fg="white")
        left_frame.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        # Create canvas and scrollbar for available seeds
        left_canvas = tk.Canvas(left_frame, bg="black", highlightthickness=0)
        left_scrollbar = tk.Scrollbar(left_frame, orient=tk.VERTICAL, command=left_canvas.yview)
        left_canvas.configure(yscrollcommand=left_scrollbar.set)
        
        # Pack canvas and scrollbar
        left_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        left_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Create frame inside canvas to hold seed items
        seeds_frame = tk.Frame(left_canvas, bg="black")
        left_canvas.create_window((0, 0), window=seeds_frame, anchor=tk.NW)
        
        # Right frame for your seeds
        right_frame = tk.LabelFrame(main_frame, text="Your Seeds", font=("Arial", 14), bg="black", fg="white")
        right_frame.pack(side=tk.RIGHT, padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        # Create canvas and scrollbar for your seeds
        right_canvas = tk.Canvas(right_frame, bg="black", highlightthickness=0)
        right_scrollbar = tk.Scrollbar(right_frame, orient=tk.VERTICAL, command=right_canvas.yview)
        right_canvas.configure(yscrollcommand=right_scrollbar.set)
        
        # Pack canvas and scrollbar
        right_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        right_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Create frame inside canvas to hold your seed items
        your_seeds_frame = tk.Frame(right_canvas, bg="black")
        right_canvas.create_window((0, 0), window=your_seeds_frame, anchor=tk.NW)
        
        # Left frame contents: available seeds
        for i, seed in enumerate(self.available_seeds):
            seed_frame = tk.Frame(seeds_frame, bg="#1A3200", bd=1, relief=tk.RIDGE, width=300)
            seed_frame.pack(fill=tk.X, padx=10, pady=5)
            
            name_label = tk.Label(seed_frame, text=seed["name"], font=("Arial", 12, "bold"), bg="#1A3200", fg="#00FF00")
            name_label.pack(anchor="w", padx=10, pady=5)
            
            desc_label = tk.Label(seed_frame, text=seed["description"], font=("Arial", 10), bg="#1A3200", fg="white", wraplength=250)
            desc_label.pack(anchor="w", padx=10, pady=5)
            
            get_btn = tk.Button(seed_frame, text="Get Seeds", font=("Arial", 10), 
                             command=lambda s=seed: self.get_seeds(s, seed_window))
            get_btn.pack(anchor="e", padx=10, pady=5)
        
        # Right frame contents: your seeds
        if not self.player_data["botany"]["seeds"]:
            empty_label = tk.Label(your_seeds_frame, text="You don't have any seeds.", font=("Arial", 12), bg="black", fg="white")
            empty_label.pack(pady=20)
        else:
            for seed in self.player_data["botany"]["seeds"]:
                seed_frame = tk.Frame(your_seeds_frame, bg="#1A3200", bd=1, relief=tk.RIDGE, width=300)
                seed_frame.pack(fill=tk.X, padx=10, pady=5)
                
                name_label = tk.Label(seed_frame, text=seed["name"], font=("Arial", 12, "bold"), bg="#1A3200", fg="#00FF00")
                name_label.pack(anchor="w", padx=10, pady=5)
                
                desc_label = tk.Label(seed_frame, text=seed["description"], font=("Arial", 10), bg="#1A3200", fg="white", wraplength=250)
                desc_label.pack(anchor="w", padx=10, pady=5)
        
        # Update scroll regions after all widgets are added
        seeds_frame.update_idletasks()
        left_canvas.config(scrollregion=left_canvas.bbox("all"))
        
        your_seeds_frame.update_idletasks()
        right_canvas.config(scrollregion=right_canvas.bbox("all"))
        
        # Make the main seeds panel visible by moving the scrollbar to the top
        left_canvas.yview_moveto(0.0)
        
        # Configure canvas resizing when window is resized
        def on_frame_configure(canvas):
            canvas.configure(scrollregion=canvas.bbox("all"))
        
        seeds_frame.bind("<Configure>", lambda e: on_frame_configure(left_canvas))
        your_seeds_frame.bind("<Configure>", lambda e: on_frame_configure(right_canvas))
        
        # Mouse wheel scrolling with focus handling
        def on_mousewheel(event, canvas):
            widget = seed_window.winfo_containing(event.x_root, event.y_root)
            # Check which canvas the mouse is over
            while widget is not None:
                if widget == left_canvas:
                    left_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
                    return
                elif widget == right_canvas:
                    right_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
                    return
                widget = widget.master
            
            # Default to left canvas if we couldn't determine
            left_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        
        # Bind mousewheel to the window so it works anywhere
        seed_window.bind("<MouseWheel>", lambda e: on_mousewheel(e, left_canvas))
        
        # Override destroy method to cleanup bindings
        orig_destroy = seed_window.destroy
        def _destroy_and_cleanup():
            try:
                seed_window.unbind("<MouseWheel>")
            except:
                pass
            orig_destroy()
        
        seed_window.destroy = _destroy_and_cleanup
        
        # Close button
        close_btn = tk.Button(seed_window, text="Close", font=("Arial", 14), width=15, command=seed_window.destroy)
        close_btn.pack(side=tk.BOTTOM, pady=10)
    
    def get_seeds(self, seed, parent_window):
        """Get seeds from the seed machine"""
        self.player_data["botany"]["seeds"].append(seed)
        
        # Show confirmation message
        messagebox.showinfo("Seeds Acquired", f"You've acquired {seed['name']}!", parent=parent_window)
        
        # Add note about getting seeds
        if "notes" not in self.player_data:
            self.player_data["notes"] = []
        
        self.player_data["notes"].append({
            "timestamp": datetime.datetime.now().isoformat(),
            "text": f"Acquired {seed['name']} from the botany seed dispenser."
        })
        
        # Refresh the seed window
        parent_window.destroy()
        self.access_seed_machine()
    
    def plant_seeds(self):
        """Plant seeds in the planters"""
        # Check if player has any seeds
        if not self.player_data["botany"]["seeds"]:
            self.botany_window.after(10, lambda: messagebox.showinfo("No Seeds", 
                                                              "You don't have any seeds to plant. Get some from the seed machine first.", 
                                                              parent=self.botany_window))
            return
        
        # Create a new toplevel window for planting
        plant_window = tk.Toplevel(self.botany_window)
        plant_window.title("Plant Seeds")
        plant_window.geometry("800x600")
        plant_window.configure(bg="black")
        plant_window.transient(self.botany_window)
        plant_window.grab_set()
        
        # Center the window
        plant_window.update_idletasks()
        width = 800
        height = 600
        x = (plant_window.winfo_screenwidth() // 2) - (width // 2)
        y = (plant_window.winfo_screenheight() // 2) - (height // 2)
        plant_window.geometry(f"{width}x{height}+{x}+{y}")
        
        # Title
        title_label = tk.Label(plant_window, text="Plant Seeds", font=("Arial", 18, "bold"), bg="black", fg="white")
        title_label.pack(pady=15)
        
        # Description
        desc_text = "Select a seed to plant and an empty planter to place it in."
        desc_label = tk.Label(plant_window, text=desc_text, font=("Arial", 12), bg="black", fg="white", wraplength=600)
        desc_label.pack(pady=10)
        
        # Top frame for seeds
        seeds_frame = tk.LabelFrame(plant_window, text="Your Seeds", font=("Arial", 14), bg="black", fg="white")
        seeds_frame.pack(padx=20, pady=10, fill=tk.X)
        
        # Keep track of the selected seed and planter
        selected_data = {"seed": None, "planter": None}
        
        # Function to select a seed
        def select_seed(seed, button):
            # Reset all seed buttons
            for btn in seed_buttons:
                btn.config(bg="#333333")
            
            # Highlight the selected button
            button.config(bg="#006600")
            
            # Update selected seed
            selected_data["seed"] = seed
            
            # Enable plant button if both seed and planter are selected
            if selected_data["planter"] is not None:
                plant_btn.config(state=tk.NORMAL)
        
        # Function to select a planter
        def select_planter(index, button):
            # Check if planter is already occupied
            if self.player_data["botany"]["planters"][index]["occupied"]:
                messagebox.showinfo("Planter Occupied", 
                                   f"Planter {index+1} already has a plant in it. Choose an empty planter.", 
                                   parent=plant_window)
                return
            
            # Reset all planter buttons
            for btn in planter_buttons:
                btn.config(bg="#333333")
            
            # Highlight the selected button
            button.config(bg="#006600")
            
            # Update selected planter
            selected_data["planter"] = index
            
            # Enable plant button if both seed and planter are selected
            if selected_data["seed"] is not None:
                plant_btn.config(state=tk.NORMAL)
        
        # Add seed options
        seed_buttons = []
        for i, seed in enumerate(self.player_data["botany"]["seeds"]):
            seed_frame = tk.Frame(seeds_frame, bg="#1A3200", bd=1, relief=tk.RIDGE)
            seed_frame.pack(fill=tk.X, padx=10, pady=5)
            
            name_label = tk.Label(seed_frame, text=seed["name"], font=("Arial", 12, "bold"), bg="#1A3200", fg="#00FF00")
            name_label.pack(side=tk.LEFT, padx=10, pady=5)
            
            select_btn = tk.Button(seed_frame, text="Select", font=("Arial", 10), bg="#333333",
                                command=lambda s=seed, b=seed_frame: select_seed(s, b))
            select_btn.pack(side=tk.RIGHT, padx=10, pady=5)
            seed_buttons.append(seed_frame)
        
        # Planter selection frame
        planters_frame = tk.LabelFrame(plant_window, text="Available Planters", font=("Arial", 14), bg="black", fg="white")
        planters_frame.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)
        
        # Add planter options
        planter_buttons = []
        for i, planter in enumerate(self.player_data["botany"]["planters"]):
            planter_frame = tk.Frame(planters_frame, bg="#222222", bd=2, relief=tk.RIDGE)
            planter_frame.pack(fill=tk.X, padx=20, pady=10)
            
            if planter["occupied"]:
                # Show occupied planter
                name_label = tk.Label(planter_frame, text=f"Planter {i+1}: {planter['plant']}", 
                                    font=("Arial", 14, "bold"), bg="#222222", fg="light green")
                name_label.pack(side=tk.LEFT, padx=10, pady=5)
                
                status_label = tk.Label(planter_frame, text="OCCUPIED", 
                                      font=("Arial", 12), bg="#222222", fg="red")
                status_label.pack(side=tk.RIGHT, padx=10, pady=5)
            else:
                # Show empty planter
                name_label = tk.Label(planter_frame, text=f"Planter {i+1}: Empty", 
                                    font=("Arial", 14, "bold"), bg="#222222", fg="white")
                name_label.pack(side=tk.LEFT, padx=10, pady=5)
                
                select_btn = tk.Button(planter_frame, text="Select", font=("Arial", 10), bg="#333333",
                                    command=lambda idx=i, b=planter_frame: select_planter(idx, b))
                select_btn.pack(side=tk.RIGHT, padx=10, pady=5)
            planter_buttons.append(planter_frame)
        
        # Function to plant the seed
        def do_planting():
            if selected_data["seed"] is None or selected_data["planter"] is None:
                return
            
            seed = selected_data["seed"]
            planter_index = selected_data["planter"]
            
            # Update the planter data
            self.player_data["botany"]["planters"][planter_index] = {
                "occupied": True,
                "plant": seed["name"],
                "growth_stage": 1  # Start at stage 1
            }
            
            # Remove the seed from inventory
            self.player_data["botany"]["seeds"].remove(seed)
            
            # Add note about planting
            if "notes" not in self.player_data:
                self.player_data["notes"] = []
            
            self.player_data["notes"].append({
                "timestamp": datetime.datetime.now().isoformat(),
                "text": f"Planted {seed['name']} in planter {planter_index+1}."
            })
            
            # Show confirmation
            messagebox.showinfo("Success", 
                             f"You've successfully planted {seed['name']} in planter {planter_index+1}.", 
                             parent=plant_window)
            
            # Close the planting window
            plant_window.destroy()
        
        # Bottom buttons
        button_frame = tk.Frame(plant_window, bg="black")
        button_frame.pack(pady=20)
        
        # Plant button (disabled until both seed and planter are selected)
        plant_btn = tk.Button(button_frame, text="Plant Seed", font=("Arial", 14), width=15, 
                           command=do_planting, state=tk.DISABLED)
        plant_btn.pack(side=tk.LEFT, padx=20)
        
        # Cancel button
        cancel_btn = tk.Button(button_frame, text="Cancel", font=("Arial", 14), width=15, 
                            command=plant_window.destroy)
        cancel_btn.pack(side=tk.LEFT, padx=20)
    
    def toggle_door_lock(self):
        """Toggle the lock on the botany lab door"""
        # Get the door location key
        door_key = "3,-1"
        
        # Get the ship map from player data
        if "ship_map" not in self.player_data:
            self.botany_window.after(10, lambda: messagebox.showinfo("Door Control", "Unable to access door control system.", parent=self.botany_window))
            return
            
        ship_map = self.player_data["ship_map"]
        if door_key not in ship_map:
            self.botany_window.after(10, lambda: messagebox.showinfo("Door Control", "Unable to access door control system.", parent=self.botany_window))
            return
            
        # Toggle the door lock
        if ship_map[door_key].get("locked", False):
            ship_map[door_key]["locked"] = False
            ship_map[door_key]["desc"] = "The station's plant cultivation and research facility. The door is unlocked."
            self.botany_window.after(10, lambda: messagebox.showinfo("Door Control", "The Botany Lab door has been unlocked.", parent=self.botany_window))
        else:
            ship_map[door_key]["locked"] = True
            ship_map[door_key]["desc"] = "The station's plant cultivation and research facility. The door is locked."
            self.botany_window.after(10, lambda: messagebox.showinfo("Door Control", "The Botany Lab door has been locked.", parent=self.botany_window))
        
        # Update ship map in player data
        self.player_data["ship_map"] = ship_map
        
        # Make sure the window stays on top after dialog
        self.botany_window.after(20, self.botany_window.lift)
        self.botany_window.focus_force()
    
    def on_closing(self):
        """Handle window closing"""
        # Check if the door is locked
        door_key = "3,-1"  # Botany Lab door
        if self.player_data.get("ship_map", {}).get(door_key, {}).get("locked", False):
            self.botany_window.after(10, lambda: messagebox.showinfo("Locked Door", "The door is locked. You must unlock it before leaving.", parent=self.botany_window))
            # Make sure the window stays on top after dialog
            self.botany_window.after(20, self.botany_window.lift)
            self.botany_window.focus_force()
            return
        
        # Release grab before closing
        self.botany_window.grab_release()
        
        # Call return callback with player data
        self.return_callback(self.player_data)
        
        # Destroy the window
        self.botany_window.destroy()
    
    def show_station_menu(self):
        """Return to main station menu options"""
        # Clear existing buttons
        for widget in self.button_frame.winfo_children():
            widget.destroy()
            
        # Check if user has special access
        is_botanist = self.player_data.get("job") == "Botanist"
        is_captain = self.player_data.get("job") == "Captain"
        is_hop = self.player_data.get("job") == "Head of Personnel"
        has_botany_access = is_botanist or is_captain or is_hop or ("permissions" in self.player_data and self.player_data["permissions"].get("botany_station", False))
        
        if has_botany_access:
            # Show station access button for authorized personnel
            station_btn = tk.Button(self.button_frame, text="Enter Botany Station", font=("Arial", 14), width=20, command=self.access_botany_station)
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