from stockfish import Stockfish
from board_to_fen.predict import get_fen_from_image_path
import sys
import cv2
import numpy as np

input_path = "./image.png"
stockfish = Stockfish("./stockfish.exe")


def get_best_move(stockfish, fen):
    stockfish.set_fen_position(fen)
    best_move = stockfish.get_best_move()
    return best_move


fen = get_fen_from_image_path(input_path)

best_move = get_best_move(stockfish, fen)
print(best_move)
