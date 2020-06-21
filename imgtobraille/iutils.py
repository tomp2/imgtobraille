"""Input Utils - Utility functions to help with getting the input"""

import os
import natsort
import errno
from urllib.request import urlopen
import cv2
import numpy as np


def assure_iterable(target):
    """Convert input to list if not already"""

    return target if isinstance(target, list) or \
                     isinstance(target, tuple) else [target]


def url_to_image(url: str):
    """Get an image from url and convert to numpy nd.array"""
    urls = assure_iterable(url)

    def to_image(url):  # Todo: refactor
        resp = urlopen(url)
        image = np.asarray(bytearray(resp.read()), dtype="uint8")
        image = cv2.imdecode(image, cv2.IMREAD_GRAYSCALE)
        return image

    return [to_image(url) for url in urls]


def get_paths(path: str) -> list:
    """
    Get list of paths for the images.
    :param path: path to folder or a file
    """
    input_path = os.path.abspath(path)
    if not os.path.exists(input_path):
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), input_path)
    if os.path.isfile(input_path):
        img_paths = [input_path]
    else:
        paths = [os.path.join(input_path, path) for path in os.listdir(input_path)]
        img_paths = natsort.natsorted(paths)
    return img_paths
