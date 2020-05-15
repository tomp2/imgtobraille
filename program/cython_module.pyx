import random


cpdef unsigned char[:,:] curves(int h, int w, unsigned char [:,:] image):
    """
    Calculates the on/off probability for the given pixel based on its value.
    Uses a function to get the chance of 1/0 and then turns it to 1/0 by
    testing it against random.random(). The output is the image which the
    on/off-status for the braille dots is read from.
    :param image: numpy.ndarray
    :param w: int
    :param h: int
    :return: numpy.ndarray
    """
    cdef int x, y, value, out
    cdef float change

    for y in range(h):
        for x in range(w):
            value = image[y, x]
            if value > 227:
                continue
            elif value < 27:
                out = 0
            else:
                value -= 127
                chance = (value - 127) ** 3 / 2000 + 50
                out = 1 if chance > random.random() else 0
            image[y, x] = out
    return image


cpdef list braille_grid(int new_height, int new_width):
    """
    Creates an 2-dimensional array with 2*4 boxes that have the coordinates of
    the corners of the specific braille character for it's location on the
    scaled image.
    :param new_width: int
    :param new_height: int
    :return: list
    """
    cdef int y_cord, x_cord
    cdef list grid

    # Make sure that the blocks fit to the image
    while new_width % 2 != 0:
        new_width -= 1
    while new_height % 4 != 0:
        new_height -= 1

    grid = []
    for y_cord in range(0, new_height, 4):
        row = [[x_cord, x_cord + 2, y_cord, y_cord + 4] for x_cord in range(0, new_width, 2)]
        grid.append(row)
    return grid


cpdef convert_to_braille(list block, unsigned char[:,:] image):
    """
    Takes the coordinates of the opposite corners of the block given, and
    forms the correct braille character from the pixels in the block.
    :param block: tuple
    :param image: numpy.ndarray
    :return: str
    """
    cdef int x_1, x_2, y_1, y_2
    cdef int y_block, y_global, x_block, x_global
    cdef int unicode_sum = 10240

    # Corners of the braille cube/block
    x_1, x_2 = block[:2]
    y_1, y_2 = block[2:]

    values = ((1, 2, 4, 64), (8, 16, 32, 128))
    for y_block, y_global in enumerate(range(y_1, y_2)):
        for x_block, x_global in enumerate(range(x_1, x_2)):
            if image[y_global, x_global]:
                unicode_sum += values[x_block][y_block]
    return chr(unicode_sum)


