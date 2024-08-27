from stockfish import Stockfish
from board_to_fen.predict import get_fen_from_image_path
import sys
import cv2
import numpy as np

image_path = "./image.png"
stockfish = Stockfish("./stockfish.exe")


def crop_chessboard(image_path):
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    blur = cv2.GaussianBlur(gray, (5, 5), 0)

    edges = cv2.Canny(blur, 50, 150)

    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    contours = sorted(contours, key=cv2.contourArea, reverse=True)

    for contour in contours:
        peri = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.02 * peri, True)

        if len(approx) == 4:
            x, y, w, h = cv2.boundingRect(approx)

            cropped_img = img[y : y + h, x : x + w]

            cv2.imwrite(image_path, cropped_img)
            return


def rotate_fen(fen):
    fen_parts = fen.split("/")
    reversed_fen_parts = [part[::-1] for part in fen_parts[::-1]]
    rotated_fen = "/".join(reversed_fen_parts)
    return rotated_fen


def get_best_move(stockfish, fen):
    stockfish.set_fen_position(fen)
    best_move = stockfish.get_best_move()
    return best_move


def draw_best_move(image, move):
    COL_MAPPING = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}

    height, width, _ = image.shape
    square_size = width // 8

    start_pos = move[:2]
    end_pos = move[2:]

    start_row = 8 - int(start_pos[1])
    start_col = COL_MAPPING[start_pos[0]]
    end_row = 8 - int(end_pos[1])
    end_col = COL_MAPPING[end_pos[0]]

    start_center = (
        start_col * square_size + square_size // 2,
        start_row * square_size + square_size // 2,
    )
    end_center = (
        end_col * square_size + square_size // 2,
        end_row * square_size + square_size // 2,
    )

    tip_length = square_size / (
        2 * np.linalg.norm(np.array(end_center) - np.array(start_center))
    )

    cv2.arrowedLine(
        image, start_center, end_center, (0, 0, 255), 2, tipLength=tip_length
    )


crop_chessboard(image_path)

original_image = cv2.imread(image_path)

fen = get_fen_from_image_path(image_path)
if not stockfish.is_fen_valid(fen + " w - - 0 1"):
    sys.exit()

best_move_white = get_best_move(stockfish, fen + " w - - 0 1")
print(best_move_white)

draw_best_move(original_image, best_move_white)

best_move_black = get_best_move(stockfish, fen + " b - - 0 1")
print(best_move_black)

draw_best_move(original_image, best_move_black)

cv2.imwrite(image_path, original_image)
