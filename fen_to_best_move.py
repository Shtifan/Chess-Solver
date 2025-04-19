import sys
import re
import argparse
from image_to_fen import ChessboardPredictor
import load_image
from config import IMAGE_PATH, STOCKFISH_PATH
import chess
import chess.engine


def shorten_fen(fen: str) -> str:
    return re.sub(r"1+", lambda m: str(len(m.group(0))), fen)


def unflip_fen(fen: str) -> str:
    rows = fen.split("/")
    return "/".join(rows[::-1])


def lengthen_fen(fen: str) -> str:
    result = ""
    for c in fen:
        if c.isdigit():
            result += "1" * int(c)
        else:
            result += c
    return result


def get_fen_from_image(invert_fen: bool = False) -> str:
    predictor = ChessboardPredictor()
    img = load_image.load_image(IMAGE_PATH)
    if img is None:
        raise Exception(f"Couldn't load image: {IMAGE_PATH}")
    img = load_image.resize_image(img)
    tiles, _ = None, None
    try:
        tiles, _ = __import__("chessboard_finder").findGrayscaleTilesInImage(img)
    except Exception as e:
        print(f"Failed to find chessboard in image: {e}")
        predictor.close()
        return None
    if tiles is None:
        print("Couldn't find chessboard in image.")
        predictor.close()
        return None
    fen, _ = predictor.get_prediction(tiles)
    predictor.close()
    
    if invert_fen:
        fen = unflip_fen(fen)
        
    return fen


def fen_to_best_moves(fen):
    fen = shorten_fen(fen)
    engine = chess.engine.SimpleEngine.popen_uci(STOCKFISH_PATH)

    board = chess.Board(fen)
    white_move = None
    if board.turn == chess.WHITE:
        result = engine.play(board, chess.engine.Limit(time=2.0))
        white_move = result.move.uci()

    if board.turn == chess.BLACK:
        result = engine.play(board, chess.engine.Limit(time=2.0))
        black_move = result.move.uci()
    else:
        black_board = chess.Board(fen)
        black_board.turn = chess.BLACK
        result = engine.play(black_board, chess.engine.Limit(time=2.0))
        black_move = result.move.uci()

    engine.quit()
    return white_move, black_move


def main():
    parser = argparse.ArgumentParser(description='Extract FEN from image and calculate best moves')
    parser.add_argument('--invert_fen', action='store_true', help='Invert FEN so white pieces are on bottom')
    parser.add_argument('--fen', help='Provide FEN directly instead of extracting from image')
    args = parser.parse_args()

    if args.fen:
        fen = args.fen
    else:
        fen = get_fen_from_image(args.invert_fen)
        
    if fen is None:
        print("Failed to extract FEN from image.")
        sys.exit(1)
        
    print(f"Predicted FEN: {fen}")
    white_move, black_move = fen_to_best_moves(fen)
    print(f"Best move for White: {white_move}")
    print(f"Best move for Black: {black_move}")
    return white_move, black_move


if __name__ == "__main__":
    main()
