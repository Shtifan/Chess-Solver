from stockfish import Stockfish
from board_to_fen.predict import get_fen_from_image_path
import sys
import cv2
import numpy as np

def get_best_move(stockfish, fen):
    stockfish.set_fen_position(fen)
    best_move = stockfish.get_best_move()
    return best_move

def rotate_fen(fen):
    fen_parts = fen.split('/')
    reversed_fen_parts = [part[::-1] for part in fen_parts[::-1]]
    rotated_fen = '/'.join(reversed_fen_parts)
    return rotated_fen

input_path = "./image.png"
output_path = "./output.png"
stockfish = Stockfish("C:/Stockfish/stockfish.exe")

#crop_chessboard(input_path)

fen = get_fen_from_image_path(input_path)
if not stockfish.is_fen_valid(fen + " w - - 0 1"):
    sys.exit()

best_move_white = get_best_move(stockfish, fen + " w - - 0 1")
print(best_move_white)

fen = rotate_fen(fen)

best_move_black = get_best_move(stockfish, fen + " b - - 0 1")
print(best_move_black)

#draw_moves(input_path,fen,best_move_black,output_path)