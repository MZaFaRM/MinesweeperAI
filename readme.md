# Minesweeper AI

This is a Python project that implements an AI agent to play Minesweeper.

## Overview

- Implements a custom Minesweeper game engine and AI agent using Pygame for graphics
- The game board, mine locations, etc are generated procedurally  
- The AI agent tracks knowledge about safe moves and uses it to play intelligently
- The user can play against the AI agent and watch it reveal squares

## Code Structure  

- `runner.py` - Main game loop, Pygame initialization, game rendering
- `minesweeper.py` - Minesweeper game logic and AI engine 
- `assets/` - Images, fonts, and other assets

## Usage

To run the game:

```
py runner.py
```


Use the mouse to reveal squares on the board. Right-click to mark potential mines. Click the "AI Move" button to have the AI agent make a move.

## Dependencies

- Python 3
- Pygame

Install requirements with: 

```
pip install -r requirements.txt
```

## Customizing

The game board size, number of mines, and other parameters can be configured by changing the constants at the top of `runner.py`. New assets can be added to the `assets/` folder. 

## License

This project is open source and licensed under the MIT License. See `LICENSE` for details.


---


<div align="center">
Made with 🧡 by Muhammed Zafar
</div>
