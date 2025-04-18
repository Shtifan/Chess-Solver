import sys
import re
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


def get_fen_from_image(image_path: str = IMAGE_PATH) -> str:
    predictor = ChessboardPredictor()
    img = load_image.load_image(image_path)
    if img is None:
        raise Exception(f"Couldn't load image: {image_path}")
    img = load_image.resize_image(img)
    tiles, _ = None, None
    try:
        tiles, _ = __import__("chessboard_finder").findGrayscaleTilesInImage(img)
    except Exception as e:
        print(f"Failed to find chessboard in image: {e}")
        predictor.close()
        return None
    if tiles is None:
        print("Couldn't find chessboard in image")
        predictor.close()
        return None
    fen, _ = predictor.get_prediction(tiles)
    predictor.close()
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
    fen = get_fen_from_image()
    if fen is None:
        print("Failed to extract FEN from image.")
        sys.exit(1)
    print(f"Predicted FEN: {fen}")
    white_move, black_move = fen_to_best_moves(fen)
    print(f"Best move for White: {white_move}")
    print(f"Best move for Black: {black_move}")


if __name__ == "__main__":
    main()
