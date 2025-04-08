# game/items.py

# Base structure for items
# { 
#     "id": "unique_item_identifier", 
#     "name": "Display Name",               
#     "description": "Item description.",
#     "category": "Category",             # e.g., Tool, Book, Healing, Junk, Food, Drink, Special
#     "attributes": {                     # Optional: Specific data for the item
#         "content": "Text of the book...", # For books
#         "heal_amount": 25,               # For healing items
#         "skill_bonus": {"engineering": 5} # Example for tools
#     },
#     "actions": ["examine", "use", "read", "drop"] # List of possible actions
# }

# --- Define Book Content --- 
# Moved from main.py
WELCOME_GUIDE_CONTENT = """WELCOME TO SPACE STATION EXPLORER

Welcome to your new home among the stars! This guide will help you get acquainted with life aboard our station.

IMPORTANT TIPS:
- Always follow safety protocols
- Report any unusual activity to Security
- Keep your personal quarters clean and organized
- Get to know your fellow crew members
- Visit the Bar for social interactions
- Check the computer terminal for stock market opportunities

We hope you enjoy your stay and contribute to our thriving community!
"""

STATION_MAP_CONTENT = """SPACE STATION EXPLORER - STATION MAP

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
"""

MAINTENANCE_MANUAL_CONTENT = """SPACE STATION MAINTENANCE MANUAL

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
"""

# --- Master Item Dictionary --- 
# Contains the base definitions for all items in the game.
# When an item is added to inventory, a copy of this definition should be used.
ALL_ITEMS = {
    # --- Tools --- 
    "wrench": {
        "id": "wrench",
        "name": "Wrench",
        "description": "Standard tool for fastening and unfastening bolts and nuts. Useful for basic engineering tasks.",
        "category": "Tool",
        "attributes": {},
        "actions": ["examine", "use", "drop"]
    },
    "screwdriver": {
        "id": "screwdriver",
        "name": "Screwdriver", 
        "description": "A multi-head screwdriver for various screw types. Essential for accessing panels and device internals.",
        "category": "Tool",
        "attributes": {},
        "actions": ["examine", "use", "drop"]
    },
    "wirecutters": {
        "id": "wirecutters",
        "name": "Wirecutters",
        "description": "Tool for cutting and stripping wires safely. Necessary for electrical work.",
        "category": "Tool",
        "attributes": {},
        "actions": ["examine", "use", "drop"]
    },
    "repair_tool": { # From random event
        "id": "repair_tool",
        "name": "Repair Tool",
        "description": "A generic multi-tool for basic repairs.",
        "category": "Tool",
        "attributes": {},
        "actions": ["examine", "use", "drop"]
    },
     "basic_tools": { # From locker
        "id": "basic_tools",
        "name": "Basic Tools",
        "description": "A set containing a small wrench, screwdriver, and pliers.",
        "category": "Tool",
        "attributes": {},
        "actions": ["examine", "use", "drop"]
    },
    "flashlight": { # From random event & locker
        "id": "flashlight",
        "name": "Flashlight",
        "description": "A standard issue flashlight. Useful in dark areas.",
        "category": "Tool", # Or maybe Utility?
        "attributes": {},
        "actions": ["examine", "use", "drop"] # 'Use' could toggle light?
    },
    "welding_tool": { # Mentioned before, adding definition
        "id": "welding_tool",
        "name": "Welding Tool",
        "description": "For joining metal components. Requires a power source.",
        "category": "Tool",
        "attributes": {},
        "actions": ["examine", "use", "drop"]
    },
    "multimeter": { # Mentioned before, adding definition
        "id": "multimeter",
        "name": "Multimeter",
        "description": "Device for measuring voltage, current, and resistance.",
        "category": "Tool",
        "attributes": {},
        "actions": ["examine", "use", "drop"]
    },
    "maintenance_tool": { # From random event
        "id": "maintenance_tool",
        "name": "Maintenance Tool",
        "description": "A generic tool used for station upkeep.",
        "category": "Tool",
        "attributes": {},
        "actions": ["examine", "use", "drop"]
    },
    "diagnostic_tool": { # From random event
        "id": "diagnostic_tool",
        "name": "Diagnostic Tool",
        "description": "A scanner used to identify issues in machinery.",
        "category": "Tool",
        "attributes": {},
        "actions": ["examine", "use", "drop"]
    },
    "portable_scanner": { # From locker
        "id": "portable_scanner",
        "name": "Portable Scanner",
        "description": "Handheld scanner for analyzing objects, environments, or life signs.",
        "category": "Tool", 
        "attributes": {},
        "actions": ["examine", "use", "drop"]
    },

    # --- Books --- 
    "welcome_guide": {
        "id": "welcome_guide",
        "name": "Welcome Guide",
        "description": "A standard issue guide for new arrivals to the station.",
        "category": "Book",
        "attributes": {
            "content": WELCOME_GUIDE_CONTENT
        },
        "actions": ["examine", "read", "drop"]
    },
    "station_map": {
        "id": "station_map",
        "name": "Station Map",
        "description": "A basic layout map of the Space Station Explorer.",
        "category": "Book",
        "attributes": {
            "content": STATION_MAP_CONTENT
        },
        "actions": ["examine", "read", "drop"]
    },
    "maintenance_manual": {
        "id": "maintenance_manual",
        "name": "Maintenance Manual",
        "description": "A technical manual covering basic maintenance and emergency procedures.",
        "category": "Book",
        "attributes": {
            "content": MAINTENANCE_MANUAL_CONTENT
        },
        "actions": ["examine", "read", "drop"]
    },
    "engineering_manual": { # From random event
        "id": "engineering_manual",
        "name": "Engineering Manual",
        "description": "A technical guide for station engineers.",
        "category": "Book",
        "attributes": {
            "content": "ENGINEERING MANUAL抜粋\nChapter 1: Power Systems - Ensure plasma flow is optimal.\nChapter 2: Atmospherics - Check filters regularly.\nChapter 3: Emergency Repairs - Use welding tool for hull breaches."
        },
        "actions": ["examine", "read", "drop"]
    },
    "navigation_chart": { # From random event
        "id": "navigation_chart",
        "name": "Navigation Chart",
        "description": "A star chart showing nearby systems.",
        "category": "Book", # Or maybe Special?
        "attributes": {
            "content": "STAR CHART - Sector 7G\nKnown Systems: Sol, Alpha Centauri, Proxima Centauri\nNebulae: Eagle Nebula\nAnomalies: Unidentified signal source near Proxima Centauri b."
        },
        "actions": ["examine", "read", "drop"]
    },
    
    # --- Healing Items ---
    "medkit": { # From random event
        "id": "medkit",
        "name": "Medkit",
        "description": "A standard first aid kit.",
        "category": "Healing",
        "attributes": {
             "heal_effect": "heal_all_limbs_full" # Placeholder logic
        },
        "actions": ["examine", "use", "drop"]
    },
    "first_aid_kit": { # From locker (same as medkit? let's alias for now)
        "id": "first_aid_kit",
        "name": "First Aid Kit",
        "description": "Basic medical supplies for minor injuries.",
        "category": "Healing",
        "attributes": {
             "heal_effect": "heal_all_limbs_full" # Placeholder logic
        },
        "actions": ["examine", "use", "drop"]
    },
    "stabilizing_agent": { # From random event
        "id": "stabilizing_agent",
        "name": "Stabilizing Agent",
        "description": "A chemical agent used to stabilize volatile reactions or patients.",
        "category": "Healing", # Or chemical?
        "attributes": {
            "heal_effect": "reduce_damage_types" # Placeholder
        },
        "actions": ["examine", "use", "drop"]
    },
    "medical_scanner": { # From random event
        "id": "medical_scanner",
        "name": "Medical Scanner",
        "description": "A handheld device for diagnosing injuries and conditions.",
        "category": "Tool", # Medical Tool
        "attributes": {},
        "actions": ["examine", "use", "drop"]
    },
     "medical_supply_kit": { # From random event
        "id": "medical_supply_kit",
        "name": "Medical Supply Kit",
        "description": "A kit containing various medical supplies.",
        "category": "Healing", 
        "attributes": {
            "contains": ["medkit", "stabilizing_agent"] # Example attribute
        },
        "actions": ["examine", "use", "drop"] # Use could unpack?
    },

    # --- Utility/Misc Items ---
    "energy_bar": { # From random event
        "id": "energy_bar",
        "name": "Energy Bar",
        "description": "A dense, nutrient-rich bar. Tastes like cardboard.",
        "category": "Food",
        "attributes": {
             "hunger_restore": 30
        },
        "actions": ["examine", "eat", "drop"]
    },
    "emergency_rations": { # From locker
        "id": "emergency_rations",
        "name": "Emergency Rations",
        "description": "Standard emergency food supply. Use only when necessary.",
        "category": "Food",
        "attributes": {
             "hunger_restore": 50
        },
        "actions": ["examine", "eat", "drop"]
    },
    "circuit_board": { # From random event
        "id": "circuit_board",
        "name": "Circuit Board",
        "description": "A standard electronic circuit board. Might be useful for repairs.",
        "category": "Component",
        "attributes": {},
        "actions": ["examine", "drop"]
    },
    "battery_pack": { # From random event
        "id": "battery_pack",
        "name": "Battery Pack",
        "description": "A replaceable power pack for various devices.",
        "category": "Component", # Or Utility?
        "attributes": {},
        "actions": ["examine", "use", "drop"] # Use could recharge something?
    },
    "power_cell": { # From random event
        "id": "power_cell",
        "name": "Power Cell",
        "description": "A standard power cell. Looks charged.",
        "category": "Component",
        "attributes": {},
        "actions": ["examine", "use", "drop"]
    },
     "id_card": { # From random event
        "id": "id_card",
        "name": "ID Card",
        "description": "A standard crew identification card. The name is smudged.",
        "category": "Special",
        "attributes": {},
        "actions": ["examine", "drop"]
    },
    "id_card_reader": { # From locker
        "id": "id_card_reader",
        "name": "ID Card Reader",
        "description": "Device to read and potentially modify crew ID cards.",
        "category": "Tool", # Security Tool
        "attributes": {},
        "actions": ["examine", "use", "drop"]
    },
    "data_pad": { # From random event
        "id": "data_pad",
        "name": "Data Pad",
        "description": "A portable electronic data storage device.",
        "category": "Special",
        "attributes": {},
        "actions": ["examine", "use", "drop"] # Use could view data?
    },
    "oxygen_canister": { # From random event
        "id": "oxygen_canister",
        "name": "Oxygen Canister",
        "description": "A small canister of breathable oxygen.",
        "category": "Utility",
        "attributes": {},
        "actions": ["examine", "use", "drop"] # Use could refill suit/mask?
    },
     "radiation_badge": { # From random event
        "id": "radiation_badge",
        "name": "Radiation Badge",
        "description": "Measures cumulative radiation exposure.",
        "category": "Utility",
        "attributes": {},
        "actions": ["examine", "drop"]
    },
    "security_pass": { # From random event
        "id": "security_pass",
        "name": "Security Pass",
        "description": "A temporary security pass. Seems expired.",
        "category": "Special",
        "attributes": {},
        "actions": ["examine", "drop"]
    },
    "security_keycard": { # From random event
        "id": "security_keycard",
        "name": "Security Keycard",
        "description": "A keycard for accessing secure areas.",
        "category": "Special", # Or Key?
        "attributes": {},
        "actions": ["examine", "use", "drop"]
    },
    "communication_device": { # From random event
        "id": "communication_device",
        "name": "Communication Device",
        "description": "A standard handheld communicator.",
        "category": "Utility",
        "attributes": {},
        "actions": ["examine", "use", "drop"]
    },
    "emergency_flare": { # From random event
        "id": "emergency_flare",
        "name": "Emergency Flare",
        "description": "A high-intensity flare for signaling.",
        "category": "Utility",
        "attributes": {},
        "actions": ["examine", "use", "drop"]
    },
    "encrypted_data_drive": { # From random event
        "id": "encrypted_data_drive",
        "name": "Encrypted Data Drive",
        "description": "A data drive protected by strong encryption.",
        "category": "Special",
        "attributes": {},
        "actions": ["examine", "use", "drop"]
    },
    "emergency_beacon": { # From locker
        "id": "emergency_beacon",
        "name": "Emergency Beacon",
        "description": "Distress signal device for emergencies. Transmits on standard frequencies.",
        "category": "Utility",
        "attributes": {},
        "actions": ["examine", "use", "drop"]
    },

    # --- Junk Items (Example) ---
    # "used_power_cell": {
    #     "id": "used_power_cell",
    #     "name": "Used Power Cell",
    #     "description": "A depleted power cell. Likely useless.",
    #     "category": "Junk",
    #     "attributes": {},
    #     "actions": ["examine", "drop"]
    # },
}

# --- Helper Functions --- 
def get_item_definition(item_id):
    """Returns a copy of the item definition from the master dictionary."""
    if item_id in ALL_ITEMS:
        return ALL_ITEMS[item_id].copy() # Return a copy to prevent modification of the original
    return None

def get_items_by_category(category_name):
    """Returns a list of item definitions for a given category."""
    return [item.copy() for item in ALL_ITEMS.values() if item["category"] == category_name] 