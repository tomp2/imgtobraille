import argparse
import errno
import os
import time

import cv2
import natsort
import tqdm

import program.cython_module as cy

# Todo:
#   merge threshold with curves?
#   colors with ANSI escape?

INFO = "[\u001b[32mi\u001b[0m]"
WARNING = "[\u001b[33m!\u001b[0m]"
ERROR = "[\u001b[31m#\u001b[0m]"


def initialize_args():
    """Initializes commandline arguments"""

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "PATH",
        action="store",
        metavar="path",
        help="Input path (file/dir)")
    parser.add_argument(
        "-w",
        action="store",
        metavar="width",
        default=100,
        type=int,
        help="Width of braille output in characters")
    parser.add_argument(
        "-t",
        action="store",
        metavar="time",
        default=0.1,
        type=float,
        help="Frame time in seconds")
    arguments = parser.parse_args()
    return arguments


def scale_image(image, new_width, old_width):
    """
    Scales an image to fit the given width
    :param image: numpy.ndarray
    :param new_width: int
    :param old_width: int
    :return: numpy.ndarray
    """
    scaling_factor = new_width / old_width  # Scale image to match given width
    image_resized = cv2.resize(                   # 2 comes from braille char width
        src=image,
        dsize=None,
        fx=scaling_factor,
        fy=scaling_factor,
        interpolation=cv2.INTER_AREA
    )
    return image_resized


def get_image_size(image):
    """
    Returns the resolution of the image given
    :param image: numpy.ndarray
    :return: tuple
    """
    # check: return type
    return image.shape[:2]


def threshold(image):
    """
    Uses OpenCV adaptiveThreshold to create an 1/0 image for the on/off-status
    for the braille dot statuses to be read from.
    Alternative to "image_filter_noise". The output is the image from  which
    the on/off-status for the braille dots is read.
    :param image: numpy.ndarray
    :return: numpy.ndarray
    """
    image_blurred = cv2.medianBlur(image, 5)
    image = cv2.adaptiveThreshold(
        src=image_blurred,
        maxValue=255,
        adaptiveMethod=cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        thresholdType=cv2.THRESH_BINARY,
        blockSize=11,
        C=2
    )
    return image


def get_input_paths(path):
    """
    Determines whether input path points to an image or a directory.
    Then returns list with the image/images.
    :param path: str
    :return: list
    :return: list
    """
    input_path = os.path.abspath(path)

    if not os.path.exists(input_path):
        print(f"{ERROR} Invalid path!")
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), input_path)
    if os.path.isfile(input_path):
        image_paths = [input_path]
    else:
        paths = [os.path.join(input_path, file) for file in os.listdir(input_path)]
        image_paths = natsort.natsorted(paths)
    return image_paths


def process_frame(path, new_width, new_height, old_width):
    """
    Forms the final braille "image" as a string.
    :param path: str
    :param new_width: int
    :param new_height: int
    :param old_width: int
    :return: str
    """
    image_original = cv2.imread(path, 0)
    image_scaled = scale_image(image_original, new_width, old_width)
    image_filtered = cy.curves(new_height, new_width, image_scaled)

    frame = []
    convert = cy.convert_to_braille
    grid = cy.braille_grid(new_height, new_width)
    for row in grid:
        row_characters = [convert(block, image_filtered) for block in row]
        frame.append(''.join(row_characters) + '\n')
    return ''.join(frame)


def preview(image):
    """
    Previes image
    :param image: numpy.ndarray
    :return: none
    """
    cv2.imshow('Image preview', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def main():
    """Main loop"""
    args = initialize_args()

    image_paths = get_input_paths(args.PATH)
    image_1 = image_paths[0]
    target_width = args.w * 2

    old_width = get_image_size(cv2.imread(image_1))[1]
    temp_scaled = scale_image(cv2.imread(image_1, 0), target_width, old_width)
    new_height, new_width = get_image_size(temp_scaled)

    ready_frames = []
    for image in tqdm.tqdm(image_paths):
        new_frame = process_frame(image, new_width, new_height, old_width)
        ready_frames.append(new_frame)

    print(ready_frames[0])
    if len(ready_frames) > 1:
        input("Play animation? [Y/n]: ")
        while True:
            for new_frame in ready_frames:
                print(new_frame)
                time.sleep(args.t)


if __name__ == "__main__":
    main()
