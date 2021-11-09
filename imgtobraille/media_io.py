from __future__ import annotations

import os
from typing import Optional, Union, Generator

import numpy as np
from cv2 import cv2
import urllib.request


def read_image_url(url: str, mode: int = 0) -> np.ndarray:
    """
    Read image file form an url to a numpy array.
    :param url: url pointing to an image file.
    :param mode: 0 for grayscale, 1 for colored.
    :return: 2d array for grayscale image, 3d array for colored image.
    """
    response = urllib.request.urlopen(url)
    content = response.read()

    original_array = np.asarray(bytearray(content), dtype=np.uint8)
    array = cv2.imdecode(original_array, mode)
    if array is None:
        raise ValueError(f"Could not decode image data from url {url}")
    return array


def read_image_file(path: str, mode: int = 0) -> np.ndarray:
    """
    Read image file to a numpy array.
    :param path:  Path to an image file.
    :param mode: 0 for grayscale, 1 for colored.
    :return: 2d array for grayscale image, 3d array for colored image.
    """
    if not os.path.isfile(path):
        raise FileNotFoundError(path)

    mode = [cv2.IMREAD_GRAYSCALE, cv2.IMREAD_COLOR][mode]
    arr = cv2.imread(path, mode)
    if arr is None:
        raise ValueError(f"Image could not be read, cv2.imread returned None for: {path}")
    if mode == cv2.IMREAD_COLOR:
        arr = cv2.cvtColor(arr, cv2.COLOR_BGR2RGB)
    return arr


class VideoStream:
    colored: bool
    source: Union[str, int]

    def __init__(self, source: Union[str, int], color: bool = False):
        self.colored = color
        self.source = source
        self.cap = cv2.VideoCapture(source)

    @property
    def source_height(self) -> int:
        return int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    @property
    def source_width(self) -> int:
        return int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))

    @property
    def current_frame(self) -> int:
        return self.cap.get(cv2.CAP_PROP_POS_FRAMES)

    def read_frame(self) -> Optional[np.ndarray]:
        flag, frame = self.cap.read()
        if flag and not self.colored:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        return frame

    def __next__(self) -> np.ndarray:
        frame = self.read_frame()
        if frame is None:
            raise StopIteration
        else:
            return frame

    def __del__(self) -> None:
        """Release video file."""
        try:
            self.cap.release()
        except AttributeError:
            pass

    def __iter__(self) -> VideoStream:
        return self

    def __enter__(self) -> VideoStream:
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Call __del__ to release video file when exiting context manager."""
        self.__del__()


class VideoFile(VideoStream):
    def __init__(self, source: str, color: bool = False):
        super().__init__(source, color)

    def read_frame(self, index: Optional[int] = None) -> Optional[np.ndarray]:
        if index is not None:
            if not 1 <= index <= self.frame_count:
                raise IndexError(
                    "read_frame index out of bounds. Trying to read"
                    f"frame {index} but video has {self.frame_count} frames"
                )
            if index != self.current_frame:
                self.goto_frame(index)

        flag, frame = self.cap.read()
        if flag and not self.colored:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        return frame

    @property
    def frame_rate(self) -> int:
        return self.cap.get(cv2.CAP_PROP_FPS)

    @property
    def frame_count(self) -> int:
        return self.cap.get(cv2.CAP_PROP_FRAME_COUNT)

    @property
    def current_frame(self) -> int:
        return self.cap.get(cv2.CAP_PROP_POS_FRAMES)

    def goto_frame(self, index) -> None:
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, index)

    def __iter__(self) -> VideoStream:
        self.goto_frame(0)
        return self

    def __getitem__(
        self, index: Union[int, slice]
    ) -> Union[Generator[Optional[np.ndarray], None, None], Optional[np.ndarray]]:
        """
        Slice aware getitem which returns a single frame.jpg or a frame.jpg generator depending
        on whether index or slice was used.
        :param index:  integer for getting single frame.jpg. Slice for range of frames/frame.jpg generator.
        :return: Single frame.jpg or frame.jpg generator.
        """
        if isinstance(index, slice):
            return (self[index] for index in range(*index.indices(self.frame_count)))
        else:
            return self.read_frame(index)
