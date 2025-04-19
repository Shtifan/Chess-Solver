import os
import sys
import subprocess
import argparse
from config import STOCKFISH_PATH, IMAGE_PATH

def main():
    parser = argparse.ArgumentParser(description='Analyze a chess position from an image and find the best moves.')
    parser.add_argument('--invert_fen', action='store_true', help='Invert FEN so white pieces are on bottom')
    args = parser.parse_args()

    print("[1/3] Extracting FEN from image...")
    fen = None
    try:
        from image_to_fen import ChessboardPredictor, unflip_fen
        import load_image

        img = load_image.load_image(IMAGE_PATH)
        if img is None:
            print(f"Couldn't load image: {IMAGE_PATH}")
            sys.exit(1)
        predictor = ChessboardPredictor()
        tiles, corners = None, None
        import chessboard_finder

        tiles, corners = chessboard_finder.findGrayscaleTilesInImage(img)
        if tiles is None:
            print("Couldn't find chessboard in image.")
            sys.exit(1)
        fen, tile_certainties = predictor.get_prediction(tiles)
        predictor.close()
        
        if args.invert_fen:
            fen = unflip_fen(fen)
            
        print(f"Predicted FEN: {fen}")
    except Exception as e:
        print(f"Error extracting FEN: {e}")
        sys.exit(1)

    print("[2/3] Getting best moves from FEN via Stockfish...")
    white_move = None
    black_move = None
    try:
        from fen_to_best_move import fen_to_best_moves

        white_move, black_move = fen_to_best_moves(fen)
        print(f"Best move for White: {white_move}")
        print(f"Best move for Black: {black_move}")
    except Exception as e:
        print(f"Error getting best moves: {e}")
        sys.exit(1)

    print("[3/3] Drawing best moves on board...")
    try:
        from draw_best_move import draw_best_move

        output_path = draw_best_move(
            white_move=white_move,
            black_move=black_move,
            output_path=os.path.join(os.path.dirname(__file__), 'solved_chessboard.png'),
            invert_fen=args.invert_fen
        )
        print(f"Saved: {output_path}")
    except Exception as e:
        print(f"Error drawing best moves: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
