import numpy as np
import PIL.Image
from io import BytesIO
import requests


def loadImageGrayscale(img_file):
    """Load image from file, convert to grayscale float32 numpy array."""
    img = PIL.Image.open(img_file)
    return img.convert("L")


def loadImageFromPath(img_path):
    """Load PIL image from image filepath, keep as color."""
    return PIL.Image.open(open(img_path, "rb"))


def loadImageFromURL(url, max_size_bytes=2000000):
    """Load PIL image from a URL, return (image, url) or (None, url) on fail."""
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        if int(response.headers.get("content-length", 0)) > max_size_bytes:
            print(
                f"Image too large to download: {response.headers.get('content-length')} bytes"
            )
            return None, url
        img = PIL.Image.open(BytesIO(response.content))
        return img, url
    except Exception as e:
        print(f"Failed to load image from URL {url}: {e}")
        return None, url


def resizeAsNeeded(img, max_size=(2000, 2000), max_fail_size=(2000, 2000)):
    """Resize if image larger than max size. Return None if above fail size."""
    if isinstance(img, np.ndarray):
        img = PIL.Image.fromarray(img)
    if img.size[0] > max_fail_size[0] or img.size[1] > max_fail_size[1]:
        return None
    if img.size[0] > max_size[0] or img.size[1] > max_size[1]:
        print(f"Image too big ({img.size[0]} x {img.size[1]})")
        new_size = np.min(max_size)
        ratio = float(new_size) / max(img.size)
        new_size_tuple = (int(img.size[0] * ratio), int(img.size[1] * ratio))
        print(f"Reducing by factor of {1.0 / ratio:.2g}")
        print(f"New size: {new_size_tuple[0]} x {new_size_tuple[1]}")
        img = img.resize(new_size_tuple, PIL.Image.BILINEAR)
    return img
