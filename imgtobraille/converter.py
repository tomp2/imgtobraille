import cv2
import numpy as np

import brailleforming
import dithering


class Braille:
    """Class to store the data of of original & converted images"""

    def __init__(self, source: str, width: int, method: int):
        self.path = source
        self.original = read_img_file(self.path)
        self.scaled = scale(self.original, width)

        height, width = self.scaled.shape[:2]
        while width % 2 != 0:
            width -= 1
        while height % 4 != 0:
            height -= 1
        self.res = (height, width, *self.original.shape)
        self.scaled = self.scaled[0:height, 0:width]

        self.frame = convert(self.scaled, method)


def convert(array, method) -> str:
    """Do the conversion from image to unicode string"""

    mat = np.asarray(array)
    dithered_mat = dither(mat, method)
    frame = to_string(dithered_mat)
    return frame


def read_img_file(source: str) -> np.ndarray:
    """Read image using open cv and return as NumPy array"""

    return cv2.imread(source, 0)


def scale(img, new_width):
    """Scale an image to fit the given width."""

    original_width = img.shape[1]

    scaling_factor = new_width / original_width
    scaled_img = cv2.resize(
        src=img,
        dsize=None,
        fx=scaling_factor,
        fy=scaling_factor,
        interpolation=cv2.INTER_AREA,
    )
    return scaled_img


def dither(img: np.ndarray, method: int = 0) -> np.ndarray:
    """Binarize image using dithering algorithm if method > 0."""

    res = img.shape[:2]
    if method == 1:
        dithered = dithering.threshold(*res, img)
    elif method == 2:
        dithered = dithering.quantize(*res, img)
    elif method == 3:
        dithered = dithering.random(*res, img)
    else:
        return img

    return dithered


def to_string(array: np.ndarray):
    """
    Convert a NumPy array to the actual image using the boolean statuses
    from the array.
    """

    res = array.shape[:2]
    grid = brailleforming.subdivide(*res)
    frame = brailleforming.form_string(grid, array)
    return frame
