import os
from typing import Iterable, List

import cv2
import numpy as np

from imgtobraille import brailleforming
from imgtobraille import dithering
from imgtobraille import iutils


class Braille:  # Todo: add image editing values
    def __init__(self, source: str, width: int = 0, method: int = 2, **kwargs):
        self.source = source
        self.args = kwargs
        self.method = method

        unscaled = read_img(self.source)[0]
        self.array = scale(unscaled, width)[0]
        # res = (old x, new y, new x)
        height, width = self.array.shape[0], width
        while width % 2 != 0:
            width -= 1
        while height % 4 != 0:
            height -= 1
        self.res = (height, width, *unscaled.shape)

        self.frame = self.convert()

    def __str__(self):
        return self.frame

    def convert(self) -> str:
        """Do the conversion from image to unicode string"""

        # Check:
        # As the fix for the resolution fitting for the rectangles is not used
        # before scaling, and only for the resolution used for operations for
        # the now (by resolution possibly different (bigger)) image, there may
        # have been happened unneeded dithering for the pixels that were left
        # remaining due to the fix happening only afterwards

        grid = brailleforming.subdivide(*self.res[0:2])
        dithered = np.asarray(dither(self.array, self.method))
        self.frame = brailleforming.form_image(grid, dithered)
        return self.frame


def read_img(source: Iterable[str]) -> List[np.ndarray]:
    """
    Convert source to numpy array
    :param source: path(s) or url(s) to images. Can be mixed.
    """

    def read_using(image: str):
        if os.path.exists(image):
            img = cv2.imread(source, 0)
        else:
            img = iutils.url_to_image(image)[0]
        return img

    sources = iutils.assure_iterable(source)

    arrays = [read_using(img) for img in sources]
    return arrays


def scale(target, width=None):
    """Scale an image to fit the given width."""
    images = iutils.assure_iterable(target)
    if not width:
        return images

    def do(image):  # Todo: refactor
        if isinstance(image, Braille):  # For Braille object:
            img = image.array
            original_width = image.res[0]
        else:                           # For np.ndarray
            original_width = image.shape[1]
            img = image

        scaling_factor = width / original_width
        scaled_img = cv2.resize(
            src=img,
            dsize=None,
            fx=scaling_factor,
            fy=scaling_factor,
            interpolation=cv2.INTER_AREA,
        )
        return scaled_img

    return [do(image) for image in images]


def dither(img: np.ndarray, method: int) -> np.ndarray:
    """Binarize image using selecting dithering algorithm."""

    # Assure that characters fit to image perfectly
    height, width = img.shape[:2]
    res = (height, width)

    if method == 1:
        dithered = dithering.threshold(*res, img)
    elif method == 2:
        dithered = dithering.quantize(*res, img)
    elif method == 3:
        dithered = dithering.random(*res, img)
    else:
        return img

    return dithered


def save():
    pass


def preview():
    pass
