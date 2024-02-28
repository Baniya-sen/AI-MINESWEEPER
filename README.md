# Minesweeper with AI

This project combines the classic Minesweeper game with artificial intelligence to intelligently decide the placement of mines on the game board.

![Minesweeper Gameplay](https://github.com/Baniya-sen/AI-MINESWEEPER/assets/144620117/b261a16b-9673-4a52-a7b6-64fabbfea59a)



## Prerequisites

Before running the game, make sure you have the following installed:
- Python 3.11 or lower
- Pygame library

You can install Pygame using pip:
```Python
      pip install pygame
  ```


## Getting Started

To run the game, simply execute the 'runner.py' file. This will launch the Minesweeper game with AI knowledge base.

## AI Knowledge Base

The AI knowledge base is represented as a set of nearby cells and the count of mines in those nearby cells. This information is used by the AI algorithm to determine the placement of mines on the game board. It's represented as: {cell1, cell2, cell3, cell4, cell5} = 2

All mines are left alone if only AI moves are used. Use single click to reveal a box and double click or 2 finger touch to mark mine.
