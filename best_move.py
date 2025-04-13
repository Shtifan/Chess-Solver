from stockfish import Stockfish
import os

def get_best_move(fen, depth=15, time_limit=1.0):
    """
    Get the best move for a given position using Stockfish.
    
    Args:
        fen (str): The FEN string representing the chess position
        depth (int): Search depth (default: 15)
        time_limit (float): Time limit in seconds (default: 1.0)
    
    Returns:
        tuple: (best_move, evaluation, top_moves)
    """
    try:
        # Initialize Stockfish (adjust the path to where Stockfish is installed)
        stockfish = Stockfish(path="stockfish")
        
        # Set engine parameters
        stockfish.set_depth(depth)
        stockfish.set_skill_level(20)  # Maximum skill level
        
        # Set the position
        if not stockfish.is_fen_valid(fen):
            raise ValueError("Invalid FEN string")
        stockfish.set_fen_position(fen)
        
        # Get the best move
        best_move = stockfish.get_best_move_time(time_limit * 1000)  # Convert to milliseconds
        
        # Get the evaluation
        evaluation = stockfish.get_evaluation()
        
        # Get top moves
        top_moves = stockfish.get_top_moves(3)
        
        return best_move, evaluation, top_moves
        
    except Exception as e:
        print(f"Error analyzing position: {str(e)}")
        return None, None, None

def analyze_from_image(image_path):
    """
    Analyze a chess position from an image and return only the best move.
    """
    # Import the FEN extractor
    from fen_extractor import get_fen_from_image
    
    # Get FEN from image
    fen = get_fen_from_image(image_path)
    if not fen:
        print("Failed to extract FEN from image")
        return
    
    # Get best move analysis
    best_move, evaluation, _ = get_best_move(fen)
    
    if best_move:
        print(f"Best Move: {best_move}")
    else:
        print("Failed to analyze position")

if __name__ == "__main__":
    # Example usage
    image_path = r"C:\Users\sstoy\Documents\Programing\Projects\Chess Solver\chessboard.jpg"
    analyze_from_image(image_path) 