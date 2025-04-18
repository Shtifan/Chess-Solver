import numpy as np

# Imports for visualization
import PIL.Image
from io import BytesIO
import requests


# All images are returned as PIL images, not numpy arrays
def loadImageGrayscale(img_file):
    """Load image from file, convert to grayscale float32 numpy array"""
    img = PIL.Image.open(img_file)

    # Convert to grayscale and return
    return img.convert("L")


def loadImageFromPath(img_path):
    """Load PIL image from image filepath, keep as color"""
    return PIL.Image.open(open(img_path, "rb"))


def loadImageFromURL(url, max_size_bytes=2000000):
    """Load PIL image from a URL, return (image, url) or (None, url) on fail."""
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        if int(response.headers.get('content-length', 0)) > max_size_bytes:
            print(f"Image too large to download: {response.headers.get('content-length')} bytes")
            return None, url
        img = PIL.Image.open(BytesIO(response.content))
        return img, url
    except Exception as e:
        print(f"Failed to load image from URL {url}: {e}")
        return None, url


def resizeAsNeeded(img, max_size=(2000, 2000), max_fail_size=(2000, 2000)):
    if not PIL.Image.isImageType(img):
        img = PIL.Image.fromarray(img)  # Convert to PIL Image if not already

    # If image is larger than fail size, don't try resizing and give up
    if img.size[0] > max_fail_size[0] or img.size[1] > max_fail_size[1]:
        return None

    """Resize if image larger than max size"""
    if img.size[0] > max_size[0] or img.size[1] > max_size[1]:
        print("Image too big (%d x %d)" % (img.size[0], img.size[1]))
        new_size = np.min(max_size)  # px
        if img.size[0] > img.size[1]:
            # resize by width to new limit
            ratio = np.float(new_size) / img.size[0]
        else:
            # resize by height
            ratio = np.float(new_size) / img.size[1]
        print("Reducing by factor of %.2g" % (1.0 / ratio))
        new_size = (np.array(img.size) * ratio).astype(int)
        print("New size: (%d x %d)" % (new_size[0], new_size[1]))
        img = img.resize(new_size, PIL.Image.BILINEAR)
    return img
