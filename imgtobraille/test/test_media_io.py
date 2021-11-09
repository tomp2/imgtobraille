from unittest import mock
from unittest.mock import MagicMock

import numpy as np
import pytest
from cv2 import cv2

from imgtobraille import media_io


def test_read_image_url():
    test_media_path = "./test_media/frame.jpg"
    with open(test_media_path, "rb") as file_obj:
        mock_content = file_obj.read()
    expected = cv2.imread(test_media_path, 0)

    with mock.patch("urllib.request.urlopen") as mock_urlopen:
        response_mock = MagicMock()
        response_mock.read.return_value = mock_content
        mock_urlopen.return_value = response_mock
        result = media_io.read_image_url("https://www.1.com/")

    assert np.array_equal(result, expected)


def test_read_image_file():
    test_media_path = "test_media/frame.jpg"
    expected1 = cv2.imread(test_media_path, 0)
    expected2 = cv2.cvtColor(cv2.imread(test_media_path, 1), cv2.COLOR_BGR2RGB)

    result1 = media_io.read_image_file(test_media_path, 0)
    result2 = media_io.read_image_file(test_media_path, 1)

    assert np.array_equal(expected1, result1)
    assert np.array_equal(expected2, result2)


def test_VideoStream():
    test_media_path = "./test_media/cube.mp4"
    stream_color = media_io.VideoStream(test_media_path, color=True)
    stream_gray = media_io.VideoStream(test_media_path, color=False)

    assert stream_gray.colored is False
    assert stream_color.colored is True

    assert stream_color.source_width == stream_gray.source_width == 120
    assert stream_color.source_height == stream_gray.source_height == 120
    assert stream_color.current_frame == stream_gray.current_frame == 0

    for frame_index in range(1, 10):
        next(stream_color)
        assert stream_color.current_frame == frame_index

    result_frame_colored = stream_color.read_frame()
    result_frame_gray = stream_gray.read_frame()
    assert result_frame_colored.shape == (120, 120, 3)
    assert result_frame_gray.shape == (120, 120)

    stream_color.cap.set(cv2.CAP_PROP_POS_FRAMES, 100)
    with pytest.raises(StopIteration):
        next(stream_color)

    stream_color.cap.set(cv2.CAP_PROP_POS_FRAMES, 89)
    assert stream_color.current_frame == 89

    assert iter(stream_color) is stream_color

    assert stream_color.read_frame() is not None
    with stream_color:
        pass
    assert stream_color.read_frame() is None


def test_VideoFile_color():
    test_media_path = "./test_media/cube.mp4"
    stream = media_io.VideoFile(test_media_path, color=True)
    print(stream.frame_count)
    with pytest.raises(IndexError):
        stream.read_frame(-1)
    with pytest.raises(IndexError):
        stream.read_frame(100)

    assert len(list(stream)) == 99

    assert stream.frame_rate == 15
    assert stream.frame_count == 99
    assert stream.current_frame == 0
    stream.read_frame(50)
    assert stream.current_frame == 50
    stream.read_frame()
    assert stream.current_frame == 50
    stream.read_frame(50)
    assert stream.current_frame == 50

    frame = stream.read_frame()
    assert frame.shape == (120, 120, 3)
