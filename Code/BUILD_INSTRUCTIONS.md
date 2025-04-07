# Space Station Explorer - Build Instructions

This document explains how to build and run the Space Station Explorer game as a standalone executable.

## Prerequisites

- Python 3.6 or higher
- Required packages (automatically installed by the build script):
  - matplotlib
  - PyInstaller

## Building the Executable

### Windows

1. Double-click on the `build.bat` file.
2. Wait for the build process to complete (this may take several minutes).
3. The executable will be created in the `dist/SpaceStationExplorer` folder.

### Manual Build

You can also manually build the executable:

1. Install required packages: `pip install -r requirements.txt`
2. Run the build script: `python build_exe.py`

## Running the Game

- Double-click the `SpaceStationExplorer.exe` file in the `dist/SpaceStationExplorer` folder.

## Save Files

The game saves will be stored in the `saves` folder alongside the executable.

This means you can copy the entire `dist/SpaceStationExplorer` folder to another location or another computer, and your save files will be preserved.

## Troubleshooting

- If the game doesn't start, try running it from the command line to see any error messages:
  - Open a command prompt in the executable's folder and type `SpaceStationExplorer.exe`

- If you get missing dependency errors during build, manually install them:
  - `pip install matplotlib pyinstaller` 