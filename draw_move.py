import cv2
import numpy as np
from best_move import analyze_from_image, get_best_move
from fen_extractor import get_fen_from_image

def draw_move(image_path, output_path=None):
    """
    Draw the best move on the chessboard image with a red arrow.
    
    Args:
        image_path (str): Path to the input chessboard image
        output_path (str, optional): Path to save the output image. If None, shows the image.
    """
    # Get FEN from image
    fen = get_fen_from_image(image_path)
    if not fen:
        print("Failed to extract FEN from image")
        return
    
    # Get best move
    best_move, _, _ = get_best_move(fen)
    if not best_move:
        print("Failed to get best move")
        return
    
    # Read the image
    img = cv2.imread(image_path)
    if img is None:
        print("Failed to read image")
        return
    
    # Get image dimensions
    height, width = img.shape[:2]
    
    # Calculate square size (assuming standard 8x8 board)
    square_size = min(height, width) // 8
    
    # Convert move to coordinates
    # Example: "e2e4" -> from e2 to e4
    from_square = best_move[:2]
    to_square = best_move[2:]
    
    # Convert algebraic notation to pixel coordinates
    def square_to_pixels(square):
        file = ord(square[0]) - ord('a')  # a=0, b=1, ..., h=7
        rank = 8 - int(square[1])         # 1=7, 2=6, ..., 8=0
        x = file * square_size + square_size // 2
        y = rank * square_size + square_size // 2
        return (x, y)
    
    start_point = square_to_pixels(from_square)
    end_point = square_to_pixels(to_square)
    
    # Draw arrow
    cv2.arrowedLine(img, start_point, end_point, (0, 0, 255), 3, tipLength=0.2)
    
    # Add move text
    font = cv2.FONT_HERSHEY_SIMPLEX
    text = f"Best Move: {best_move}"
    cv2.putText(img, text, (10, 30), font, 1, (0, 0, 255), 2)
    
    if output_path:
        cv2.imwrite(output_path, img)
        print(f"Image saved to {output_path}")
    else:
        cv2.imshow("Chess Board with Best Move", img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

if __name__ == "__main__":
    # Example usage
    image_path = r"C:\Users\sstoy\Documents\Programing\Projects\Chess Solver\chessboard.jpg"
    draw_move(image_path)
