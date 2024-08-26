from stockfish import Stockfish
from board_to_fen.predict import get_fen_from_image_path
import sys
import cv2
import numpy as np

image_path = "./image.png"
stockfish = Stockfish("./stockfish.exe")


fen = get_fen_from_image_path(image_path)
if not stockfish.is_fen_valid(fen + " w - - 0 1"):
    sys.exit()


stockfish.set_fen_position(fen)

best_move = stockfish.get_best_move()
print(best_move)
