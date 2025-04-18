import numpy as np
import PIL.Image


def load_grayscale(img_file):
    img = PIL.Image.open(img_file)
    return img.convert("L")


def load_image(img_path):
    return PIL.Image.open(open(img_path, "rb"))


def resize_image(img, max_size=(2000, 2000), max_fail_size=(2000, 2000)):
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
