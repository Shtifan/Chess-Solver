# Chess Solver

A tool that analyzes chess positions from images, finds the best moves using Stockfish, and visualizes them.

## Quick Start

1. Install dependencies:
    ```
    pip install -r requirements.txt
    ```
2. Make sure Stockfish and your model are in the `assets` folder (or update `config.py`).

3. Run the main script:
    ```
    python src/chess_solve.py [--invert_fen]
    ```

## What It Does

-   Detects a chessboard and pieces from an image
-   Converts the position to FEN notation
-   Uses Stockfish to find the best moves
-   Draws the moves on the image

## Configuration

Edit `config.py` to set paths for:

-   Input image
-   Output image
-   Stockfish engine
-   Model

## Requirements

-   Python 3
-   TensorFlow
-   NumPy
-   Pillow
-   python-chess
-   Stockfish engine
