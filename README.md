# Chess Solver

A computer vision and AI-powered tool that analyzes chess positions from images, finds the best moves using Stockfish, and visualizes them on the board.

## Overview

Chess Solver automates the process of:
1. Detecting a chessboard in an image
2. Recognizing the position (pieces and their locations)
3. Converting the position to FEN notation
4. Finding the best moves for both white and black using Stockfish
5. Drawing the moves back onto the original image with colored arrows

## Features

- **Computer Vision**: Detects chessboards and pieces from images using machine learning
- **Chess Engine Integration**: Uses Stockfish to calculate optimal moves
- **Move Visualization**: Shows best moves with colored arrows (red for white, blue for black)
- **FEN Inversion**: Option to invert the board orientation ensuring white pieces are always at the bottom

## Installation

1. Clone this repository
2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Make sure Stockfish is correctly located in the project directory (or update the path in config.py)

## Usage

### Basic Usage

Run the main script with:

```
python chess_solve.py
```

This will analyze the default image specified in config.py and output a solved image.

### Command-Line Options

The following scripts support command-line arguments:

#### chess_solve.py

```
python chess_solve.py [--invert_fen]
```

- `--invert_fen`: Invert the board FEN to ensure white pieces are on the bottom

#### image_to_fen.py

```
python image_to_fen.py [--invert_fen]
```

- `--invert_fen`: Invert the board FEN to ensure white pieces are on the bottom

#### fen_to_best_move.py

```
python fen_to_best_move.py [--invert_fen] [--fen FEN_STRING]
```

- `--invert_fen`: Invert the board FEN to ensure white pieces are on the bottom
- `--fen`: Provide a FEN string directly instead of extracting from an image

#### draw_best_move.py

```
python draw_best_move.py --white_move MOVE [--black_move MOVE] [--invert_fen]
```

- `--white_move`: The best move for white in UCI format (e.g., "e2e4")
- `--black_move`: The best move for black in UCI format (e.g., "e7e5")
- `--invert_fen`: Invert the board FEN to ensure white pieces are on the bottom

### Configuration

Edit the `config.py` file to modify:
- Input image path
- Output image path
- Stockfish engine path
- Model path

## How It Works

1. `chess_solve.py` orchestrates the process by calling the other modules
2. `image_to_fen.py` handles the computer vision part:
   - Detects the chessboard in the image
   - Identifies each piece using a trained neural network
   - Generates a FEN string representing the position
3. `fen_to_best_move.py` processes the chess position:
   - Takes the FEN representation
   - Passes it to the Stockfish engine
   - Gets the best moves for both white and black
4. `draw_best_move.py` visualizes the results:
   - Draws red arrows for white's best move
   - Draws blue arrows for black's best move
   - Outputs the annotated image

## Requirements

- Python 3.8–3.11
- TensorFlow
- NumPy
- Pillow (PIL)
- python-chess
- Stockfish chess engine
