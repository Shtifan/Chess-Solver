import re
from helper_functions import shortenFEN
from message_template import *


def lengthenFEN(fen):
    # Expand FEN notation (e.g., 3k4 -> 111k1111)
    result = ""
    for c in fen:
        if c.isdigit():
            result += "1" * int(c)
        else:
            result += c
    return result
