import os
import re
import argparse
import numpy as np
import PIL.Image
import tensorflow as tf
import load_image
import chessboard_finder
from config import IMAGE_PATH


def shorten_fen(fen: str) -> str:
    return re.sub(r"1+", lambda m: str(len(m.group(0))), fen)


def unflip_fen(fen: str) -> str:
    rows = fen.split("/")
    return "/".join(rows[::-1])


def lengthen_fen(fen: str) -> str:
    result = ""
    for c in fen:
        if c.isdigit():
            result += "1" * int(c)
        else:
            result += c
    return result


def load_graph(model_filepath: str) -> tf.Graph:
    try:
        with tf.io.gfile.GFile(model_filepath, "rb") as f:
            graph_def = tf.compat.v1.GraphDef()
            graph_def.ParseFromString(f.read())
    except Exception as e:
        print(f"Error loading graph file '{model_filepath}': {e}")
        raise
    with tf.compat.v1.Graph().as_default() as graph:
        tf.compat.v1.import_graph_def(graph_def, name="tcb")
    return graph


class ChessboardPredictor:
    def __init__(self, model_path: str = None):
        from config import MODEL_PATH
        if model_path is None:
            model_path = MODEL_PATH
        graph = load_graph(model_path)
        self.sess = tf.compat.v1.Session(graph=graph)
        self.x = graph.get_tensor_by_name("tcb/Input:0")
        self.keep_prob = graph.get_tensor_by_name("tcb/KeepProb:0")
        self.prediction = graph.get_tensor_by_name("tcb/prediction:0")
        self.probabilities = graph.get_tensor_by_name("tcb/probabilities:0")

    def get_prediction(self, tiles: np.ndarray) -> tuple:
        if tiles is None or len(tiles) == 0:
            print("Couldn't parse chessboard")
            return None, 0.0
        validation_set = np.swapaxes(np.reshape(tiles, [32 * 32, 64]), 0, 1)
        guess_prob, guessed = self.sess.run(
            [self.probabilities, self.prediction],
            feed_dict={self.x: validation_set, self.keep_prob: 1.0},
        )
        a = np.array(list(map(lambda x: x[0][x[1]], zip(guess_prob, guessed))))
        tile_certainties = a.reshape([8, 8])[::-1, :]
        label_index2_name = lambda label_index: " KQRBNPkqrbnp"[label_index]
        piece_names = ["1" if k == 0 else label_index2_name(k) for k in guessed]
        fen = "/".join(
            ["".join(piece_names[i * 8 : (i + 1) * 8]) for i in reversed(range(8))]
        )
        return fen, tile_certainties

    def make_prediction(self, url: str) -> list:
        img, url = load_image.load_image(url)
        result = [None, None, None]
        if img is None:
            print(f'Couldn\'t load URL: "{url}"')
            return result
        img = load_image.resize_image(img)
        if img is None:
            print(f'Image too large to resize: "{url}"')
            return result
        tiles, corners = chessboard_finder.findGrayscaleTilesInImage(img)
        if tiles is None:
            print("Couldn't find chessboard in image.")
            return result
        fen, tile_certainties = self.get_prediction(tiles)
        certainty = tile_certainties.min()
        visualize_link = None
        result = [fen, certainty, visualize_link]
        return result

    def close(self) -> None:
        self.sess.close()


def main() -> None:
    parser = argparse.ArgumentParser(description='Extract FEN from a chessboard image')
    parser.add_argument('--invert_fen', action='store_true', help='Invert FEN so white pieces are on bottom')
    args = parser.parse_args()
    
    unflip = args.invert_fen
    active = "w"
    
    img = load_image.load_image(IMAGE_PATH)
    if img is None:
        raise Exception(f"Couldn't load image: {IMAGE_PATH}")
    tiles, corners = chessboard_finder.findGrayscaleTilesInImage(img)
    if tiles is None:
        raise Exception("Couldn't find chessboard in image.")
    predictor = ChessboardPredictor()
    fen, tile_certainties = predictor.get_prediction(tiles)
    predictor.close()
    
    if unflip:
        fen = unflip_fen(fen)
        
    short_fen = shorten_fen(fen)
    certainty = tile_certainties.min()
    print("Per-tile certainty:")
    print(tile_certainties)
    print(
        f"Certainty range [{tile_certainties.min()} - {tile_certainties.max()}], Avg: {tile_certainties.mean()}"
    )
    print(f"---\nPredicted FEN:\n{short_fen} {active} - - 0 1")
    print(f"Final Certainty: {certainty * 100:.1f}%")
    
    return short_fen


if __name__ == "__main__":
    np.set_printoptions(suppress=True, precision=3)
    main()
