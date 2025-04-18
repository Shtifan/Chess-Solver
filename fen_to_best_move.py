import sys
import re
from image_to_fen import ChessboardPredictor
from stockfish import Stockfish
import image_loading
from config import IMAGE_PATH, STOCKFISH_PATH


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
    img = image_loading.loadImageFromPath(image_path)
    if img is None:
        raise Exception(f"Couldn't load image: {image_path}")
    img = image_loading.resizeAsNeeded(img)
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


def get_best_move(fen: str, stockfish_path: str = STOCKFISH_PATH) -> str:
    stockfish = Stockfish(path=stockfish_path)
    stockfish.set_fen_position(fen)
    return stockfish.get_best_move()


def main():
    fen = get_fen_from_image()
    if fen is None:
        print("Failed to extract FEN from image.")
        sys.exit(1)
    print(f"Predicted FEN: {fen}")
    best_move = get_best_move(fen)
    print(f"Best move: {best_move}")


if __name__ == "__main__":
    main()
