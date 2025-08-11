# Enhanced Python Chess GUI

A feature-rich chess application built with Python and Tkinter that supports human vs human, human vs engine, and engine vs engine gameplay.

## Features

- **Multiple Game Modes**:
  - Player vs Player
  - Player vs Engine
  - Engine vs Engine (automated battles)

- **Advanced Gameplay**:
  - Full chess rule validation
  - Move history with scrollable list
  - Visual move highlighting
  - Last move indication
  - Undo functionality
  - Save/Load game functionality

- **Engine Integration**:
  - Support for any UCI-compatible chess engine
  - Configurable engine strength (1-20 levels)
  - Adjustable thinking time
  - Dual engine support for engine battles

- **Enhanced UI**:
  - Modern dark theme with professional styling
  - Unicode chess pieces with shadow effects
  - Coordinate labels (a-h, 1-8)
  - Responsive button design
  - Status indicators for engine state

## Requirements

- Python 3.7 or higher
- Required Python packages (install via `pip install -r requirements.txt`)
- A UCI-compatible chess engine (Stockfish recommended)

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/top-site/chess
   cd chess-gui
   ```

2. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Install a chess engine**:
   
   **Option A: Stockfish (Recommended)**
   - Download from [Stockfish Official Website](https://stockfishchess.org/download/)
   - Extract and place the executable in your PATH, or note the full path
   
   **Option B: Other UCI Engines**
   - Download any UCI-compatible engine (Komodo, Leela, etc.)
   - Note the path to the executable

4. **Configure the engine path**:
   - Open `chessgui4.py` in a text editor
   - Update the `engine_path` variable (line 14) with your engine's path:
     ```python
     self.engine_path = "stockfish"  # or full path like "/path/to/stockfish"
     ```

## Usage

Run the application:
```bash
python chessgui4.py
```

### Game Controls

- **Click** pieces to select and move them
- **New Game**: Start a fresh game
- **Undo Move**: Take back the last move
- **Save Game**: Export move history to a text file
- **Load Game**: Import and replay a saved game
- **Engine Battle**: Watch engines play against each other

### Game Modes

1. **Player vs Engine**: Human plays as White, engine as Black
2. **Player vs Player**: Two humans take turns
3. **Engine vs Engine**: Automated battle between two engine instances

### Engine Settings

- **Time Limit**: Set thinking time per move (0.1-60 seconds)
- **Engine Strength**: Adjust difficulty level (1-20)
- **Mode Selection**: Choose your preferred game mode

## Saved Game Format

Games are saved as text files containing UCI move notation:
```
e2e4
e7e5
g1f3
b8c6
...
```

## Troubleshooting

### Engine Not Found
- Ensure your chess engine is properly installed
- Check that the `engine_path` in `chessgui4.py` points to the correct executable
- Try using the full path to the engine instead of just the filename

### Permission Errors
- On Unix systems, make sure the engine executable has execute permissions:
  ```bash
  chmod +x /path/to/your/engine
  ```

### Performance Issues
- Reduce engine thinking time for faster moves
- Lower engine strength level for quicker decisions
- Close other resource-intensive applications

## Technical Details

- **Chess Logic**: Powered by the `python-chess` library
- **GUI Framework**: Built with Tkinter (cross-platform)
- **Engine Communication**: UCI protocol support
- **Threading**: Non-blocking engine calculations
- **File Formats**: Plain text move notation for game saves

## Contributing

Feel free to submit issues and pull requests. Some areas for improvement:
- Additional chess variants support
- PGN format import/export
- Online play capabilities
- Advanced engine analysis features

## License

This project is open source. Please check the license file for details.

---

**Note**: This application requires a separate chess engine installation. The GUI itself handles the interface and game logic, while the engine provides move calculations and analysis.
