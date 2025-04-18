import os
import sys
import subprocess
from config import IMAGE_PATH, STOCKFISH_PATH

print("[1/3] Extracting FEN from image...")
fen = None
try:
    from image_to_fen import ChessboardPredictor
    import image_loading

    img = image_loading.loadImageFromPath(IMAGE_PATH)
    if img is None:
        print(f"Couldn't load image: {IMAGE_PATH}")
        sys.exit(1)
    predictor = ChessboardPredictor()
    tiles, corners = None, None
    import chessboard_finder

    tiles, corners = chessboard_finder.findGrayscaleTilesInImage(img)
    if tiles is None:
        print("Couldn't find chessboard in image")
        sys.exit(1)
    fen, tile_certainties = predictor.get_prediction(tiles)
    predictor.close()
    print(f"Predicted FEN: {fen}")
except Exception as e:
    print(f"Error extracting FEN: {e}")
    sys.exit(1)

print("[2/3] Getting best move from FEN via Stockfish...")
best_move = None
try:
    from stockfish import Stockfish

    stockfish = Stockfish(STOCKFISH_PATH)
    stockfish.set_fen_position(fen)
    best_move = stockfish.get_best_move()
    print(f"Best move: {best_move}")
except Exception as e:
    print(f"Error getting best move: {e}")
    sys.exit(1)

print("[3/3] Drawing best move on board...")
try:
    from draw_best_move import draw_best_move

    output_path = draw_best_move(IMAGE_PATH, best_move)
    print(f"Saved: {output_path}")
except Exception as e:
    print(f"Error drawing best move: {e}")
    sys.exit(1)
