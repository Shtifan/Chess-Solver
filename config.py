import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(ROOT_DIR, "saved_models")
STOCKFISH_PATH = os.path.join(ROOT_DIR, "stockfish.exe")
IMAGE_PATH = os.path.join(ROOT_DIR, "chessboard.jpg")
OUTPUT_PATH = os.path.join(ROOT_DIR, "solved.png")
