from typing import Optional
from typing import Union, Literal

import numba as nb
import numpy as np
from cv2 import cv2


@nb.njit(cache=True)
def _calculate_box_fitting_scaling_factor(
    arr: np.ndarray, max_width: Optional[int] = None, max_height: Optional[int] = None
) -> float:
    if max_width is None and max_height is None:
        raise ValueError("Must provide either width or height.")
    elif (
        max_width is not None
        and max_width < 1
        or max_height is not None
        and max_height < 1
    ):
        raise ValueError("Image can't be less that 1x1.")

    image_height, image_width = arr.shape[:2]
    if max_height is not None and max_width is not None:
        aspect_ratio = image_width / image_height
        if image_width / max_width > image_height / max_height:
            scaling_factor = max_width / aspect_ratio / image_height
        else:
            scaling_factor = max_height * aspect_ratio / image_width
    elif max_width is not None:
        scaling_factor = max_width / image_width
    elif max_height is not None:
        scaling_factor = max_height / image_height
    else:
        raise ValueError("Invalid max_width or max_height provided.")
    return scaling_factor


def fit_in_box(
    arr: np.ndarray, max_width: Optional[int] = None, max_height: Optional[int] = None
) -> np.ndarray:
    """
    Scale a 2D numpy array so that it fits in a box defined by max_width & max_height.
    Aspect ratio will not be changed.
    """
    scaling_factor = _calculate_box_fitting_scaling_factor(arr, max_width, max_height)
    return cv2.resize(
        src=arr,
        dsize=None,
        fx=scaling_factor,
        fy=scaling_factor,
        interpolation=cv2.INTER_NEAREST,
    )


def rgb_to_grayscale(arr: np.ndarray) -> np.ndarray:
    return cv2.cvtColor(arr, cv2.COLOR_BGR2GRAY)


def fl_dithering(
    arr: np.ndarray,
    threshold: Union[int, float, Literal["mean"]] = 175,
    quant_err_multiplier: float = 0.8,
) -> np.ndarray:
    """
    Black/White Floyd–Steinberg dithering, heavy loops with numba.

    :param arr: array to dither
    :param threshold: cutoff (from range 0-255) for whether a dot is on/off.
    :return: a new dithered array.
    :param quant_err_multiplier: Multiplies the quant error. Value below 1 reduces the
    amount of error distributed to nearby cells, which might result in more contrasted look.
    Value of 0 would disable error diffusion and dithering resulting in thresholding only.
    """
    if threshold == "mean":
        threshold = np.mean(arr)

    # Must use bigger datatype than int8 to prevent integer overflow when
    # diffusing error to cells with big values already.
    padded = np.pad(array=arr, pad_width=1, mode="constant").astype("int16")
    return _fl_dithering(
        arr=padded,
        threshold=threshold,
        low=0,
        high=255,
        quant_err_multiplier=quant_err_multiplier,
    )


@nb.njit(cache=True, fastmath=True)
def _fl_dithering(
    arr: np.ndarray, threshold: float, low: int, high: int, quant_err_multiplier: float
) -> np.ndarray:
    """Actual implementation for heavy loops of `fl_dithering` with numba."""
    if len(arr.shape) > 2:
        raise ValueError(f"Array input must be 2-Dimensional.")
    height, width = arr.shape[:2]
    for y in range(1, height - 1):
        for x in range(1, width - 1):
            old_pixel = arr[y, x]
            new_pixel = high if old_pixel > threshold else low
            arr[y, x] = new_pixel
            quant_error = (old_pixel - new_pixel) * quant_err_multiplier
            arr[y, x + 1] += round(quant_error * 0.4375)
            arr[y + 1, x - 1] += round(quant_error * 0.1875)
            arr[y + 1, x] += round(quant_error * 0.3125)
            arr[y + 1, x + 1] += round(quant_error * 0.0625)
    return np.clip(arr[1:-1, 1:-1], 0, 255)


def crop_edges(arr: np.ndarray, thresh: int = 1) -> np.ndarray:
    """
    Drop the rows and columns with all values below given threshold.

    [[0, 0, 0, 0, 0]
     [0, 1, 1, 1, 0]
     [0, 1, 1, 1, 0]     [[1, 1, 1]
     [0, 1, 1, 1, 0]      [1, 1, 1]
     [0, 0, 0, 0, 0]] ->  [1, 1, 1]]
    """
    above_thresh = np.argwhere(arr > thresh).T
    top = np.min(above_thresh[0])
    bottom = np.max(above_thresh[0])
    left = np.min(above_thresh[1])
    right = np.max(above_thresh[1])
    return arr[top : bottom + 1, left : right + 1]
