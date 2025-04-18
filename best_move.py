from stockfish import Stockfish
import os

def get_best_move(fen, depth=15, time_limit=1.0):
    """
    Get the best move for a given position using Stockfish.
    """
    if not fen:
        print("Error: No FEN string provided")
        return None, None, None
        
    try:
        # Initialize Stockfish
        stockfish = Stockfish(path="stockfish.exe")
        
        # Set engine parameters
        stockfish.set_depth(depth)
        stockfish.set_skill_level(20)
        
        # Clean and validate FEN
        fen = fen.strip()
        print(f"Analyzing position: {fen}")
        
        if not stockfish.is_fen_valid(fen):
            print(f"Invalid FEN format: {fen}")
            return None, None, None
            
        stockfish.set_fen_position(fen)
        
        # Get the best move with time limit
        best_move = stockfish.get_best_move_time(int(time_limit * 1000))
        if not best_move:
            print("No legal moves found")
            return None, None, None
            
        # Get evaluation and top moves
        evaluation = stockfish.get_evaluation()
        top_moves = stockfish.get_top_moves(3)
        
        return best_move, evaluation, top_moves
        
    except Exception as e:
        print(f"Error in Stockfish analysis: {str(e)}")
        if "stockfish" in str(e).lower():
            print("Make sure stockfish.exe is in the same directory")
        return None, None, None

def analyze_from_image(image_path):
    """
    Analyze a chess position from an image.
    """
    from fen_extractor import get_fen_from_image
    
    print(f"Analyzing image: {image_path}")
    fen = get_fen_from_image(image_path)
    
    if not fen:
        print("Failed to extract FEN from image")
        return
    
    best_move, evaluation, top_moves = get_best_move(fen)
    
    if best_move:
        print(f"\nAnalysis Results:")
        print(f"Best Move: {best_move}")
        print(f"Evaluation: {evaluation}")
        if top_moves:
            print("\nTop 3 Moves:")
            for move in top_moves:
                print(f"- {move}")
    else:
        print("Failed to find best move")

if __name__ == "__main__":
    image_path = r"C:\Users\sstoy\Documents\Programing\Projects\Chess Solver\chessboard.jpg"
    analyze_from_image(image_path)