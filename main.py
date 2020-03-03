import random
import statistics
import time
import os
import natsort
from PIL import Image
from tqdm import tqdm


def initialize_args():
    """Initializes commandline arguments"""
    import argparse
    parser = argparse.ArgumentParser()
    input_group = parser.add_mutually_exclusive_group(required=True)
    parser.add_argument(
        "-w",
        action="store",
        default=120,
        type=int,
        help="Width of braille output")
    parser.add_argument(
        "-f",
        action="store",
        metavar="time",
        default=0.1,
        type=float,
        help="frame time in seconds")
    input_group.add_argument(
        "-p",
        action="store",
        metavar="Path",
        help="folder with images")
    input_group.add_argument(
        "-i",
        action="store",
        metavar="image",
        help="only one image")
    arguments = parser.parse_args()
    return arguments


def pixel_status(pixel_brightness):
    """
    Get 1/0 status for pixel by probability
    :param pixel_brightness: int
    :return: boolean
    """
    if pixel_brightness < 90:
        cap = 0
    elif pixel_brightness > 180:
        cap = 100
    else:
        cap = 1

    chance = cap * pixel_brightness / 255 * 100 * 1.4
    pixel_brightness = True if chance > random.randint(2, 100) else False
    return pixel_brightness


def get_pixel_status(x, y, image):
    """
    Convert pixel values to on/off (True/False)
    :param x: int,  (actual image pos)
    :param y: int,  (actual image pos)
    :param image: pillow image obj
    :return: boolean
    """
    rbg_values = image.getpixel((x - 1, y - 1))[:-1]
    value = pixel_status(statistics.mean(rbg_values))
    return value


def make_grids(file, path, size):
    """
    -Creates a grid with same resolution as the image to store pixel statuses
    -Sections that grid to 2*8 (braille character) sized squares
    :param file: str    image filename
    :param path: str    path to image (without filename)
    :param size: list   image resolution
    :return: tuple      (list, dict)
    """
    try:
        with Image.open(path + file) as image:
            image.thumbnail(size)
            if not os.path.isdir("animation/"):
                os.mkdir("animation/")
            image.save("animation/" + file)
    except IOError as error:
        print("Error when scaling image:", file)
        raise error

    outfile = "animation/" + file
    with Image.open(outfile) as image:
        width = image.size[0]
        while width % 2 != 0:
            width -= 1
        height = image.size[1]
        while height % 4 != 0:
            height -= 1

        status_grid = []
        for y in range(1, height + 1):
            row = [get_pixel_status(x, y, image) for x in range(1, width + 1)]
            status_grid.append(row)

    braille_grid = {}
    for i, y in enumerate(range(0, height, 4)):
        braille_grid[i + 1] = [(x, x + 2, y, y + 4) for x in range(0, width, 2)]

    return status_grid, braille_grid


def get_pixel_character(xx_yy, matrix):
    """
    Calculates local coordinates from braille set coordinate-blocks
    to calculate sum for unicode character value
    :param xx_yy: tuple     e.g.(0, 0, 3, 6)
    :param matrix: dict
    :return: str
    """
    unicode_sum = 0
    for y_l, y_g in enumerate(range(xx_yy[2], xx_yy[3])):
        for x_l, x_g in enumerate(range(xx_yy[0], xx_yy[1])):
            if matrix[y_g][x_g]:
                if x_l == 0 and y_l == 0:
                    unicode_sum += 1
                elif x_l == 0 and y_l == 1:
                    unicode_sum += 2
                elif x_l == 0 and y_l == 2:
                    unicode_sum += 4
                elif x_l == 0 and y_l == 3:
                    unicode_sum += 64
                elif x_l == 1 and y_l == 0:
                    unicode_sum += 8
                elif x_l == 1 and y_l == 1:
                    unicode_sum += 16
                elif x_l == 1 and y_l == 2:
                    unicode_sum += 32
                else:
                    unicode_sum += 128

    unicode_sum += 10240
    unicode_character = chr(unicode_sum)
    return unicode_character


def main():
    """Main loop"""
    args = initialize_args()
    width = args.w
    path = args.p

    if args.i:
        animation = []
        frame = []
        on_off_grid, braille_grid = make_grids(args.i, "", (width, width))
        for row in braille_grid.values():
            row_unicode = [get_pixel_character(x, on_off_grid) for x in row]
            frame.append(''.join(row_unicode) + '\n')
        animation.append(''.join(frame) + "\nStop by pressing CTRL+C")
    else:
        animation = []
        for image in tqdm(natsort.natsorted(os.listdir(path))):
            frame = []
            on_off_grid, braille_grid = make_grids(image, path, (width, width))
            for row in braille_grid.values():
                row_unicode = [get_pixel_character(x, on_off_grid) for x in row]
                frame.append(''.join(row_unicode) + '\n')
            animation.append(''.join(frame) + "\nStop by pressing CTRL+C")

    if len(animation) > 1:
        while True:
            for img in animation:
                print(img)
                time.sleep(args.f)
    else:
        print(animation[0])


if __name__ == "__main__":
    main()
