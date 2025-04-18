# TensorFlow Chessbot (ChessFENBot)

A Python tool that uses TensorFlow to detect chessboards in images (from file or URL) and predict the FEN (Forsyth-Edwards Notation) string representing the board position. Useful for extracting chess positions from screenshots, online boards, or photos.

## Features
- Detects chessboards in arbitrary images using computer vision.
- Uses a trained TensorFlow CNN to recognize pieces and generate a FEN string.
- Supports both local image files and URLs.
- Outputs per-tile certainty and overall certainty of prediction.

## Requirements
- Python 3.8–3.11
- Install dependencies:
  ```bash
  pip install -r requirements.txt
  ```

## Usage

### Predict FEN from an image
Run the main script to predict the FEN from an image file or URL:

```bash
python tensorflow_chessbot.py --filepath path/to/image.png
# or
python tensorflow_chessbot.py --url https://example.com/chessboard.png
```

**Options:**
- `--filepath`: Path to a local image file.
- `--url`: URL of an image.
- `--unflip`: If set, revert the image of a flipped chessboard.
- `--active`: Specify which side to play (default: w).

### Example Output
```
---
Predicted FEN:
rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w - - 0 1
Final Certainty: 98.5%
```
