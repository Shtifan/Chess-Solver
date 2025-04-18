import numpy as np
from PIL import Image, ImageDraw
import chessboard_finder
import load_image
from config import IMAGE_PATH, OUTPUT_PATH


def algebraic_to_coords(square):
    file = ord(square[0].lower()) - ord("a")
    rank = int(square[1]) - 1
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
    return img.crop((y0, x0, y1, x1))


def draw_best_move(
    image_path=IMAGE_PATH, white_move=None, black_move=None, output_path=None
):
    img = load_image.load_image(image_path)
    if img is None:
        raise ValueError(f"Couldn't load image: {image_path}")

    img_arr = np.asarray(img.convert("L"), dtype=np.float32)
    corners = chessboard_finder.findChessboardCorners(img_arr)
    if corners is None:
        raise ValueError("Couldn't find chessboard in image.")
    
    original_img = img.convert("RGB")
    draw = ImageDraw.Draw(original_img)
    
    x0, y0, x1, y1 = corners
    
    board_width = x1 - x0
    board_height = y1 - y0
    square_w = board_width / 8
    square_h = board_height / 8

    if white_move:
        src, dst = white_move[:2], white_move[2:]
        src_file, src_rank = algebraic_to_coords(src)
        dst_file, dst_rank = algebraic_to_coords(dst)

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
        src_file, src_rank = algebraic_to_coords(src)
        dst_file, dst_rank = algebraic_to_coords(dst)

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

    draw.rectangle([(y0, x0), (y1, x1)], outline=(0, 255, 0), width=2)

    if output_path is None:
        output_path = OUTPUT_PATH
    original_img.save(output_path)
    return output_path


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 3:
        print(
            "Usage: python draw_best_move.py <image_path> <white_move> [black_move] [output_path]"
        )
        sys.exit(1)
    image_path = sys.argv[1] if len(sys.argv) > 1 else IMAGE_PATH
    white_move = sys.argv[2]
    black_move = sys.argv[3] if len(sys.argv) > 3 else None
    output_path = sys.argv[4] if len(sys.argv) > 4 else None
    out = draw_best_move(image_path, white_move, black_move, output_path)
    print(f"Saved: {out}")
