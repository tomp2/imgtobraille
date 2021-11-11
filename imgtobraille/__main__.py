import argparse
import errno
import os
import shutil
import time
from typing import Optional, Sequence

import natsort

from imgtobraille import arr_filters
from imgtobraille import media_io
from imgtobraille import render


def initialize_args(*args: Optional[Sequence[str]]) -> argparse.Namespace:
    """
    Parse cli arguments.
    :param args: Override cli arguments by giving
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "PATH",
        action="store",
        metavar="path",
        help="Path to file or directory",
    )
    parser.add_argument(
        "-dims",
        action="store",
        metavar="dimensions",
        nargs="+",
        type=int,
        default=list(),
        help="width and height of output as characters. Use 0 for automatic terminal width/height",
    )
    parser.add_argument(
        "-e",
        action="store",
        metavar="diffusion",
        default=0.8,
        type=float,
        help="error diffusion level, range 0-1. 0=no dithering, 1=full error diffusion.",
    )
    parser.add_argument(
        "-fps",
        action="store",
        metavar="fps",
        default=25,
        type=float,
        help="Fps for animation",
    )
    parser.add_argument(
        "-p",
        action="store_true",
        default=False,
        help="Whether to prerender all frames before animating.",
    )
    parsed_args = parser.parse_args([*args]) if args else parser.parse_args()

    if not 1 <= len(parsed_args.dims) <= 2:
        msg = f'Argument "-dims" takes at least 1 values and at most 2 values'
        parser.error(msg)
    if any(value < 0 for value in parsed_args.dims):
        msg = f'Argument "-dims" values must not be negative.'
        parser.error(msg)

    return parsed_args


def get_paths(path: str) -> list:
    """Get a list of images from cli args."""
    abspath = os.path.abspath(path)
    if not os.path.exists(abspath):
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), abspath)
    if os.path.isfile(abspath):
        return [abspath]
    paths = [os.path.join(abspath, filename) for filename in os.listdir(abspath)]
    return natsort.natsorted(paths)


def renderer(args):
    file, (image_width, image_height), dithering = args
    arr = media_io.read_image_file(file, 0)
    arr = arr_filters.fit_in_box(arr, image_width, image_height)
    arr = arr_filters.fl_dithering(arr, quant_err_multiplier=dithering)
    return render.render(arr)


def main():
    args = initialize_args()

    files = get_paths(args.PATH)
    if not files:
        raise ValueError(f"No file(s) found at {files}")
    arg_dimensions = args.dims
    dithering = args.e
    frametime = 1 / args.fps

    missing_axes = 2 - len(arg_dimensions)
    arg_dimensions.extend([0] * missing_axes)
    if 0 in arg_dimensions:
        terminal_size = shutil.get_terminal_size()
        arg_dimensions = [
            argument or fallback
            for argument, fallback in zip(arg_dimensions, terminal_size)
        ]

    image_resolution = (arg_dimensions[0] * 2, arg_dimensions[1] * 4)
    frame_count = len(files)
    frame_generator = (renderer((file, image_resolution, dithering)) for file in files)
    if frame_count == 1:
        print(next(frame_generator))
    elif frame_count > 1:
        if args.p:
            ready_frames = list(frame_generator)
        else:
            ready_frames = []
            for frame in frame_generator:
                print(frame)
                time.sleep(frametime)
                ready_frames.append(frame)

        while True:
            for frame in ready_frames:
                print(frame)
                time.sleep(frametime)
    else:
        print("No frames were rendered.")


if __name__ == "__main__":
    main()
