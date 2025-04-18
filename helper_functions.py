import numpy as np
import PIL.Image


def shortenFEN(fen):
    # Replace consecutive 1s with a number
    import re

    return re.sub(r"1+", lambda m: str(len(m.group(0))), fen)


def unflipFEN(fen):
    # Unflip FEN string for flipped chessboards
    rows = fen.split("/")
    return "/".join(rows[::-1])
