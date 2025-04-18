import numpy as np
from PIL import Image, ImageDraw
import chessboard_finder
import image_loading
from config import IMAGE_PATH


def algebraic_to_coords(square):
    """Convert algebraic notation (e.g. 'e4') to (file, rank) indices (0-based, a1=0,0)."""
    file = ord(square[0].lower()) - ord("a")
    rank = 8 - int(square[1])
    return file, rank


def draw_arrow(draw, start, end, color=(255, 0, 0), width=4, arrowhead=18):
    """Draw a clean, symmetrical arrow with open head from start to end on a PIL ImageDraw object."""
    import math

    draw.line([start, end], fill=color, width=width)
    dx = end[0] - start[0]
    dy = end[1] - start[1]
    angle = math.atan2(dy, dx)
    length = math.hypot(dx, dy)
    headlen = min(arrowhead, length * 0.4)
    # Open arrowhead (two lines)
    for side in [-1, 1]:
        angle2 = angle + side * math.radians(28)
        x2 = end[0] - headlen * math.cos(angle2)
        y2 = end[1] - headlen * math.sin(angle2)
        draw.line([end, (x2, y2)], fill=color, width=width)


def crop_chessboard(img, corners):
    """Crop the chessboard region from the image using corners [x0,y0,x1,y1]."""
    x0, y0, x1, y1 = corners
    return img.crop((y0, x0, y1, x1))


def draw_best_move(image_path=IMAGE_PATH, move=None, output_path=None):
    """
    Draws the best move as a red arrow on a cropped chessboard image.
    Args:
        image_path (str): Path to the input image containing a chessboard.
        move (str): Move in algebraic notation, e.g. 'e7e8'.
        output_path (str): Path to save the output image. If None, appends '_arrow' to the filename.
    Returns:
        output_path (str): Path to the saved image with arrow.
    """
    # Load image
    img = image_loading.loadImageFromPath(image_path)
    if img is None:
        raise ValueError(f"Couldn't load image: {image_path}")

    # Find chessboard corners
    img_arr = np.asarray(img.convert("L"), dtype=np.float32)
    corners = chessboard_finder.findChessboardCorners(img_arr)
    if corners is None:
        raise ValueError("Couldn't find chessboard in image.")

    # Crop chessboard
    cropped = crop_chessboard(img, corners)
    cropped = cropped.convert("RGB")
    draw = ImageDraw.Draw(cropped)

    # Calculate square size
    w, h = cropped.size
    square_w = w / 8
    square_h = h / 8

    # Parse move
    src, dst = move[:2], move[2:]
    src_file, src_rank = algebraic_to_coords(src)
    dst_file, dst_rank = algebraic_to_coords(dst)

    # Center of source and destination squares
    src_xy = (src_file * square_w + square_w / 2, src_rank * square_h + square_h / 2)
    dst_xy = (dst_file * square_w + square_w / 2, dst_rank * square_h + square_h / 2)

    # Draw arrow
    draw_arrow(
        draw,
        src_xy,
        dst_xy,
        color=(255, 0, 0),
        width=max(2, int(min(square_w, square_h) // 10)),
        arrowhead=int(min(square_w, square_h) // 2.5),
    )

    # Save output
    if not output_path:
        output_path = image_path.rsplit(".", 1)[0] + "_arrow.png"
    cropped.save(output_path)
    return output_path


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 3:
        print("Usage: python draw_best_move.py <image_path> <move> [output_path]")
        sys.exit(1)
    image_path = sys.argv[1] if len(sys.argv) > 1 else IMAGE_PATH
    move = sys.argv[2]
    output_path = sys.argv[3] if len(sys.argv) > 3 else None
    out = draw_best_move(image_path, move, output_path)
    print(f"Saved: {out}")
