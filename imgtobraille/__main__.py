"""CLI Program"""

import argparse
import errno
import os
import time
from typing import Optional, Sequence

import natsort

import converter


def initialize_args(*args: Optional[Sequence[str]]) -> argparse.Namespace:
    """
    Initialize commandline arguments.
    :param args: args to pass to parser. Overrides cli arguments
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'PATH',
        action='store',
        metavar='path',
        help='Input path (file/dir)',
    )
    parser.add_argument(
        '-w',
        action='store',
        metavar='width',
        default=100,
        type=int,
        help='Width of print in characters',
    )
    parser.add_argument(
        '-d',
        action='store',
        metavar='dithering',
        default=2,
        type=int,
        help='1=threshold, 2=Floyd–Steinberg, 3=random, 4=none',
    )
    parser.add_argument(
        '-t',
        action='store',
        metavar='time',
        default=0.05,
        type=float,
        help='Frame time in seconds',
    )
    return parser.parse_args([*args]) if args else parser.parse_args()


def get_paths(path: str) -> list:
    """
    Get the path to a single image, or all the paths to all image files inside a folder.
    Finally, return a list with the paths.
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


def main():
    """Run main loop."""
    args = initialize_args()

    paths = get_paths(args.PATH)

    brailles = [converter.Braille(path, width=args.w * 2, method=args.d) for path in paths]

    if len(brailles) > 1 and input('Play animation? [Y/n]: ') in 'Yy':
        while True:
            for braille in brailles:
                print(braille.frame)
                time.sleep(args.t)
    else:
        print(brailles[0].frame)


if __name__ == '__main__':
    main()
