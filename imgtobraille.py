"""Main program."""
import argparse
import errno
import os
import sys
import time

import cv2
import natsort
import numpy as np
import tqdm

from source import dithering
from source import brailleforming
from source.visual import good, bad, info, silent


def initialize_args() -> argparse.Namespace:
    """Initialize commandline arguments."""
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
    parser.add_argument(
        '-s',
        action='store_true',
        default=False,
        help='Silent',
    )
    return parser.parse_args()


def preview_ndarray(img: np.ndarray) -> None:
    """Preview image."""
    cv2.imshow('Image preview_ndarray', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def save_frames_txt(frames: list, separator: str = '\n\n') -> None:
    """Save converted frames to a text file."""
    with open('frames', 'w') as save_file:
        save_file.write(separator.join(frames))


def get_input_paths(path: str) -> list:
    """Get list of paths for the images."""

    input_path = os.path.abspath(path)
    if not os.path.exists(input_path):
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), input_path)
    if os.path.isfile(input_path):
        img_paths = [input_path]
    else:
        paths = [os.path.join(input_path, path) for path in os.listdir(input_path)]
        img_paths = natsort.natsorted(paths)

    return img_paths


class Scaling:
    """Handles the part where image files are relevant. """

    def __init__(self, paths: list, target_width: int) -> None:
        """Get old and new resolutions to use in scaling and looping."""
        self.paths = paths
        self.target_width = target_width

        img_unscaled = cv2.imread(self.paths[0], 0)
        self.unscaled_res = img_unscaled.shape[:2]

    def scale_img(self, path: str) -> np.ndarray:
        """Scale an image to fit the given width."""
        img = cv2.imread(path, 0)
        scaling_factor = self.target_width / self.unscaled_res[1]

        return cv2.resize(
            src=img,
            dsize=None,
            fx=scaling_factor,
            fy=scaling_factor,
            interpolation=cv2.INTER_AREA,
        )

    def get_scaled(self) -> list:
        """Return all images scaled."""

        return [
            self.scale_img(img) for img in tqdm.tqdm(
                self.paths,
                unit=' f',
                disable='-s' in sys.argv,
                ascii=True,
            )
        ]


class Converting:
    """Do dithering and conversion to output string."""

    def __init__(self, images: list, method: int) -> None:
        """Subdivide canvas and fit resolution for it."""
        self.images = images
        self.method = method

        # Update res to allow dithering to function better near the borders
        # In the end the image will have these proportions
        height, width = images[0].shape[:2]
        while width % 2 != 0:
            width -= 1
        while height % 4 != 0:
            height -= 1
        self.scaled_res = (height, width)

        self.grid = brailleforming.subdivide(*self.scaled_res)

    def dithering(self, img: np.ndarray, method: int) -> np.ndarray:
        """Binarize image using selecting dithering algorithm."""
        if method == 1:
            dithered = dithering.threshold(*self.scaled_res, img)
        elif method == 2:
            dithered = dithering.quantize(*self.scaled_res, img)
        elif method == 3:
            dithered = dithering.random(*self.scaled_res, img)
        else:
            return img

        return dithered

    def process_frame(self, img: np.ndarray) -> str:
        """Turn the image to a string for output."""
        # Subdivide to rectangles
        dithered = self.dithering(img, method=self.method)
        return brailleforming.form_image(self.grid, dithered)

    def get_frames(self) -> list:
        """Return all processed frames as strings for output."""
        return [
            self.process_frame(img) for img in tqdm.tqdm(
                self.images,
                unit=' f',
                disable='-s' in sys.argv,
                ascii=True,
            )
        ]


def main():
    """Run main loop."""
    verbose = '-s' not in sys.argv
    locals()['good'] = good if verbose else silent
    locals()['bad'] = bad if verbose else silent
    locals()['info'] = info if verbose else silent

    args = initialize_args()

    print(good('Getting image path(s)'))
    paths = get_input_paths(args.PATH)
    print(good(f'Found {len(paths)} images'))

    scaler = Scaling(paths, args.w)
    print(good(f'Original width {scaler.unscaled_res[0]} '
               f'will be scaled to {scaler.target_width}'))

    print(good('Scaling images'))
    scaled_images = scaler.get_scaled()

    converter = Converting(scaled_images, args.d)
    height, width = scaler.unscaled_res
    print(good(f'Final res: {width // 2}*{height // 4} characters'))

    ready_frames = converter.get_frames()


    print(ready_frames[0])

    save_frames_txt(ready_frames)

    if len(ready_frames) > 1 and input('Play animation? [Y/n]: ') in 'Yy':
        while True:
            for new_frame in ready_frames:
                print(new_frame)
                time.sleep(args.t)


if __name__ == '__main__':
    main()
