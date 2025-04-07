import tkinter as tk
from tkinter import ttk
import json
import os

class CharacterCreation:
    def __init__(self, parent_window, game_ready_callback):
        # Create a new toplevel window
        self.creation_window = tk.Toplevel(parent_window)
        self.creation_window.title("Create Your Character")
        self.creation_window.geometry("600x500")
        
        # Store references
        self.parent_window = parent_window
        self.game_ready_callback = game_ready_callback
        
        # Initialize player data
        self.player_data = {}
        
        # Create main frame with padding
        self.main_frame = ttk.Frame(self.creation_window, padding="20")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(
            self.main_frame,
            text="Character Creation",
            font=("Arial", 16, "bold")
        )
        title_label.pack(pady=10)
        
        # Name input
        name_frame = ttk.Frame(self.main_frame)
        name_frame.pack(fill=tk.X, pady=10)
        
        name_label = ttk.Label(
            name_frame,
            text="Character Name:",
            font=("Arial", 12)
        )
        name_label.pack(side=tk.LEFT, padx=5)
        
        self.name_entry = ttk.Entry(
            name_frame,
            width=30,
            font=("Arial", 12)
        )
        self.name_entry.pack(side=tk.LEFT, padx=5)
        
        # Job selection
        job_frame = ttk.LabelFrame(
            self.main_frame,
            text="Select Your Job",
            padding="10"
        )
        job_frame.pack(fill=tk.X, pady=10)
        
        # Job options
        self.selected_job = tk.StringVar()
        
        jobs = [
            ("Staff Assistant", "General crew member - 1000 credits"),
            ("Engineer", "Maintain the station's systems and equipment - 2500 credits"),
            ("Security Guard", "Protect the station and maintain order - 5000 credits"),
            ("Doctor", "Treat injuries and keep the crew healthy - 7500 credits"),
            ("Captain", "Command the station and its crew - 10000 credits")
        ]
        
        for i, (job, description) in enumerate(jobs):
            job_option = ttk.Frame(job_frame)
            job_option.pack(fill=tk.X, pady=5)
            
            job_radio = ttk.Radiobutton(
                job_option,
                text=job,
                variable=self.selected_job,
                value=job,
                command=self.update_job_description
            )
            job_radio.pack(side=tk.LEFT)
            
            job_desc = ttk.Label(
                job_option,
                text=description,
                font=("Arial", 10)
            )
            job_desc.pack(side=tk.LEFT, padx=10)
        
        # Job description
        self.job_desc_frame = ttk.LabelFrame(
            self.main_frame,
            text="Job Description",
            padding="10"
        )
        self.job_desc_frame.pack(fill=tk.X, pady=10)
        
        self.job_description = ttk.Label(
            self.job_desc_frame,
            text="Select a job to see its description.",
            font=("Arial", 10),
            wraplength=500
        )
        self.job_description.pack(pady=10)
        
        # Start button
        self.start_button = ttk.Button(
            self.main_frame,
            text="Start Game",
            command=self.start_game
        )
        self.start_button.pack(pady=20)
    
    def update_job_description(self):
        """Update the job description based on selected job"""
        job = self.selected_job.get()
        
        if job == "Engineer":
            description = "Engineers are responsible for keeping the station's critical systems operational. " + \
                         "They excel at repairing equipment and solving technical problems. " + \
                         "Starting with 2500 credits and access to the Engineering Station."
        elif job == "Staff Assistant":
            description = "Staff Assistants are the backbone of daily station operations. " + \
                         "They handle various tasks as needed across the station. " + \
                         "Starting with 1000 credits."
        elif job == "Security Guard":
            description = "Security Guards maintain order and protect the station from threats. " + \
                         "They have access to security systems and equipment. " + \
                         "Starting with 5000 credits and access to the Security Station."
        elif job == "Doctor":
            description = "Doctors provide medical care to the station's crew. " + \
                         "They can diagnose and treat a variety of conditions. " + \
                         "Starting with 7500 credits and access to the MedBay Station."
        elif job == "Captain":
            description = "The Captain is the highest authority on the station. " + \
                         "They make critical decisions and coordinate all departments. " + \
                         "Starting with 10000 credits and access to all station areas."
        else:
            description = "Select a job to see its description."
        
        self.job_description.config(text=description)
    
    def start_game(self):
        """Create the character and start the game"""
        name = self.name_entry.get().strip()
        job = self.selected_job.get()
        
        # Validate inputs
        if not name:
            tk.messagebox.showerror("Error", "Please enter a character name.")
            return
        
        if not job:
            tk.messagebox.showerror("Error", "Please select a job.")
            return
        
        # Create character data
        self.player_data["name"] = name
        self.player_data["job"] = job
        
        # Set starting credits based on job
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
        else:
            self.player_data["credits"] = 1000  # Default starting credits
            
        self.player_data["inventory"] = []  # Empty inventory
        
        # Set job-specific permissions for room access
        if job == "Captain":
            # Captain has access to all stations
            self.player_data["permissions"] = {
                "security_station": True,
                "medbay_station": True,
                "bridge_station": True,
                "engineering_station": True
            }
        else:
            # Other jobs have specific access
            self.player_data["permissions"] = {
                "security_station": job == "Security Guard",
                "medbay_station": job == "Doctor",
                "bridge_station": job == "Captain",
                "engineering_station": job == "Engineer"
            }
        
        # Save the game right after character creation
        from game.game import Game
        Game.save_game(self.player_data)
        
        # Destroy the character creation window
        self.creation_window.destroy()
        
        # Start the game with the created character
        self.game_ready_callback(self.player_data) 