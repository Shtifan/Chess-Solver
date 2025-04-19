import numpy as np
from PIL import ImageDraw
import chessboard_finder
import load_image
import argparse
from config import IMAGE_PATH, OUTPUT_PATH


def algebraic_to_coords(square, invert_fen=False):
    file = ord(square[0].lower()) - ord("a")
    rank = int(square[1]) - 1
    if invert_fen:
        return file, rank  
    else:
        return file, 7 - rank  


def draw_arrow(draw, start, end, color=(255, 0, 0), width=4, arrowhead=18):
    import math

    bg_color = color + (180,)

    dx = end[0] - start[0]
    dy = end[1] - start[1]
    angle = math.atan2(dy, dx)
    length = math.hypot(dx, dy)

    draw.line([start, end], fill=color, width=width)

    headlen = min(arrowhead, length * 0.4)

    for side in [-1, 1]:
        angle2 = angle + side * math.radians(30)
        x2 = end[0] - headlen * math.cos(angle2)
        y2 = end[1] - headlen * math.sin(angle2)
        draw.line([end, (x2, y2)], fill=color, width=width)


def crop_chessboard(img, corners):
    x0, y0, x1, y1 = corners
    return img.crop((x0, y0, x1, y1))


def draw_best_move(
    white_move=None, black_move=None, output_path=None, invert_fen=False
):
    img = load_image.load_image(IMAGE_PATH)
    if img is None:
        raise ValueError(f"Couldn't load image: {IMAGE_PATH}")

    img_arr = np.asarray(img.convert("L"), dtype=np.float32)
    corners = chessboard_finder.findChessboardCorners(img_arr)
    if corners is None:
        raise ValueError("Couldn't find chessboard in image..")
    
    cropped_img = crop_chessboard(img.convert("RGB"), corners)
    draw = ImageDraw.Draw(cropped_img)
    x0, y0, x1, y1 = 0, 0, cropped_img.height, cropped_img.width  
    board_width = y1 - y0
    board_height = x1 - x0
    square_w = board_width / 8
    square_h = board_height / 8

    if white_move:
        src, dst = white_move[:2], white_move[2:]
        src_file, src_rank = algebraic_to_coords(src, invert_fen)
        dst_file, dst_rank = algebraic_to_coords(dst, invert_fen)
        src_xy = (
            y0 + src_file * square_w + square_w / 2,
            x0 + src_rank * square_h + square_h / 2,
        )
        dst_xy = (
            y0 + dst_file * square_w + square_w / 2,
            x0 + dst_rank * square_h + square_h / 2,
        )
        draw_arrow(
            draw,
            src_xy,
            dst_xy,
            color=(255, 0, 0),
            width=max(2, int(min(square_w, square_h) // 10)),
            arrowhead=int(min(square_w, square_h) // 2.5),
        )

    if black_move:
        src, dst = black_move[:2], black_move[2:]
        src_file, src_rank = algebraic_to_coords(src, invert_fen)
        dst_file, dst_rank = algebraic_to_coords(dst, invert_fen)
        src_xy = (
            y0 + src_file * square_w + square_w / 2,
            x0 + src_rank * square_h + square_h / 2,
        )
        dst_xy = (
            y0 + dst_file * square_w + square_w / 2,
            x0 + dst_rank * square_h + square_h / 2,
        )
        draw_arrow(
            draw,
            src_xy,
            dst_xy,
            color=(0, 0, 255),
            width=max(2, int(min(square_w, square_h) // 10)),
            arrowhead=int(min(square_w, square_h) // 2.5),
        )

    draw.rectangle([(0, 0), (cropped_img.width - 1, cropped_img.height - 1)], outline=(0, 255, 0), width=2)

    if output_path is None:
        output_path = OUTPUT_PATH
    cropped_img.save(output_path)
    return output_path


if __name__ == "__main__":
    import sys

    parser = argparse.ArgumentParser(description="Draw the best moves on a chessboard image.")
    parser.add_argument('--invert_fen', action='store_true', help='Invert FEN so black pieces are on bottom')
    parser.add_argument('--white_move', required=True, help='The best move for white in UCI format (e.g. "e2e4")')
    parser.add_argument('--black_move', help='The best move for black in UCI format (e.g. "e7e5")')
    args = parser.parse_args()
    white_move = args.white_move
    black_move = args.black_move
    out = draw_best_move(white_move, black_move, OUTPUT_PATH, invert_fen=args.invert_fen)
    print(f"Saved: {out}")
