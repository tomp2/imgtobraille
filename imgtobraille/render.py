from typing import Optional

import numba as nb
import numpy as np

BRAILLE_CODEPOINT_START: int = 10240
ANSI_RESET_COLORS: str = "\033[0m"
BRAILLE_TILE: np.ndarray = np.array([[1, 8], [2, 16], [4, 32], [64, 128]])


@nb.njit(cache=True)
def get_shape_for_tile_split(
    arr_height: int, arr_width: int, nchannels: int, tile_height: int, tile_width: int
) -> list[int]:
    """
    Calculate the shape for array so that it can be split into tiles by giving
    the calculated shape to numpy reshape.
    :param arr_height: height of the input array.
    :param arr_width: width of the input array.
    :param nchannels: number of color channels in the input array.
    :param tile_height: desired height of tile.
    :param tile_width: desired width of tile.
    :return: list of integers to give as an argument to numpy reshape.
    """
    shape = [
        arr_height // tile_height,
        tile_height,
        arr_width // tile_width,
        tile_width,
    ]
    if nchannels > 1:
        shape.append(nchannels)
    return shape


def split_to_tiles(array: np.ndarray, tile_height: int, tile_width: int) -> np.ndarray:
    """
    Reshape the given array into rows and columns of (tile_width * tile_height * channels) tiles.
    Thus 2d input array will result in 4-dimensional output, and 3d input (image with colors)
    will result in 5-dimensional output.

    :param array: 2- or 3-dimensional numpy array.
    :param tile_height: desired height of tile.
    :param tile_width: desired width of tile.
    :return: a 2d array containing one or more tiles per cell.
    """
    arr_height, arr_width, *dimensions = array.shape
    nchannels = dimensions[0] if dimensions else 1
    new_shape = get_shape_for_tile_split(
        arr_height, arr_width, nchannels, tile_height, tile_width
    )
    return array.reshape(new_shape).swapaxes(1, 2)


def colorize_string(string: str, r: int, g: int, b: int, *, reset: bool = True) -> str:
    """
    Colorize the input string with ansi escape sequence.
    Rgb inputs are not checked to be in the valid range 0-255.
    :param r: red value from range 0-255.
    :param g: green value from range 0-255.
    :param b: blue value from range 0-255.
    :param string: string that should be colorized.
    :param reset: whether to reset the color back to normal after the string.
    :return: Color formatted string.
    """
    # Todo: optimize sequential characters with same colors.
    output = f"\u001b[38;2;{r};{g};{b}m{string}"
    if reset:
        output += "\033[0m"
    return output


def colorize_view(
    str_matrix: np.ndarray, color_matrix: np.ndarray, rstrip: bool = True
) -> str:
    """
    Colorize a string matrix characters using color_matrix that has the same resolution.
    color_matrix is a 3d array containing the same amount of rows and columns. Each cell
    has 3 values: red, green and blue. RGB values are used to create an ANSI escape sequence
    to give a color to a string. Rows are joined to create a single multiline string.
    :param str_matrix: a 2d matrix of strings
    :param color_matrix: a 3d matrix with same height and width as str_matrix, and also a 3rd
    dimension for rgb values.
    :param rstrip: whether to strip invisible characters from ends of rows.
    :return: Colored multiline string.
    """
    rows = (
        "".join(
            colorize_string(braille, *color_matrix[y, x], reset=False)
            for x, braille in enumerate(char_row)
        )
        for y, char_row in enumerate(str_matrix)
    )
    if rstrip:
        rows_formatted = (line.rstrip(chr(BRAILLE_CODEPOINT_START)) for line in rows)
    else:
        rows_formatted = rows
    return "\n".join(rows_formatted) + ANSI_RESET_COLORS


def _validate_render_arguments(
    dot_arr: np.ndarray, color_arr: Optional[np.ndarray]
) -> None:
    """
    Validate the arguments that are passed to `render`. Value errors are raised when
    argument values are invalid.
    :param dot_arr: array that determines the on/off status of braille dots.
    :param color_arr: optional array that will be used to color the
    braille characters with ansi escape sequences.
    :return:
    """
    if len(dot_arr.shape) != 2:
        raise ValueError(f"dot_arr must be 2-dimensional. Shape was {dot_arr.shape}")
    if color_arr is not None:
        if len(color_arr.shape) != 3:
            raise ValueError(
                f"color_arr must be 3-dimensional. Shape was {dot_arr.shape}"
            )
        if color_arr.shape[2] != 3:
            raise ValueError(
                "color_arr's 3rd dimension should have length of 3. color_arr "
                f"should be an image with 3 color channels. Shape was {dot_arr.shape}"
            )
        if dot_arr.shape[:2] != color_arr.shape[:2]:
            raise ValueError(
                "dot_arr and color_arr must have the same height and width: "
                f"gray_arr.shape={dot_arr.shape} != {color_arr.shape}"
            )

    height_arr, width_arr = dot_arr.shape
    if height_arr < 4 or width_arr < 2:
        raise ValueError(
            "Height must be greater than 3 and width must be greater than 1."
        )


def render(
    dot_arr: np.ndarray,
    color_arr: Optional[np.ndarray] = None,
    rstrip: bool = True,
    tile: np.ndarray = BRAILLE_TILE,
) -> str:
    """
    Create a braille unicode representation of a numpy array. dot_arr will be
    used to form the braille unicode characters. One pixel/value in dot_arr equals
    one dot in braille character. If color_arr is given, the output braille characters
    will also be colored with ANSI escape codes.
    :param dot_arr: array that determines the on/off status of braille dots.
    :param color_arr: optional array that will be used to color the
    braille characters with ansi escape sequences.
    :param rstrip: whether to strip invisible characters from ends of rows.
    :param tile: braille tile.
    :return:
    """
    _validate_render_arguments(dot_arr, color_arr)

    arr_height, arr_width = dot_arr.shape
    tile_height, tile_width = tile.shape

    # Braille tiles must fit over the array without leaving a remainder
    dot_arr = dot_arr[arr_height % tile_height :, arr_width % tile_width :]
    if color_arr is not None:
        color_arr = color_arr[arr_height % 4 :, arr_width % 2 :]

    # Divide array(s) into a list of tiles
    tiled_array = split_to_tiles(dot_arr, tile_height, tile_width)

    # Clip values of tiles to 0/1 and multiply with `tile`
    masked_bits = np.clip(tiled_array, 0, 1, out=tiled_array) * tile

    # New array which contains the sums of each tiles values
    tile_sums = masked_bits.sum(axis=(2, 3)).astype(
        np.int64
    )  # Todo: check if astype is needed

    # Add to get the right offset for unicode braille code point
    tile_sums += BRAILLE_CODEPOINT_START

    # Join characters to rows, and rows with a linebreak
    if color_arr is None:
        rows = (
            row.astype("int32").view(dtype=f"U{row.size}").item() for row in tile_sums
        )
        if rstrip:
            rows_formatted = (line.rstrip(chr(BRAILLE_CODEPOINT_START)) for line in rows)
        else:
            rows_formatted = rows
        return "\n".join(rows_formatted)
    else:
        # If colored array is provided, each color channel is split to tiles, similarly to the gray array.
        # For each braille character there are 3 tiles from separate red, green and blue channels.
        # Averages of a tile from each 3 channels gives 3 values, rgb. Those will be used
        # to create and ANSI escape sequence to give a color to the corresponding braille character.
        colored_tile_means = (
            split_to_tiles(color_arr, tile_height, tile_width)
            .mean(axis=(2, 3))
            .astype(int)
        )

        # View the tile sum array as unicode. View contains the braille characters
        unicode_buf = tile_sums.view("U2")
        return colorize_view(unicode_buf, colored_tile_means)
