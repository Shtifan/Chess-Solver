import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(ROOT_DIR, "model.pb")
STOCKFISH_PATH = os.path.join(ROOT_DIR, "stockfish.exe")
IMAGE_PATH = os.path.join(ROOT_DIR, "chessboard.png")
OUTPUT_PATH = os.path.join(ROOT_DIR, "solved_chessboard.png")
