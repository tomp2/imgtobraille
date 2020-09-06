"""Cython"""

cpdef list subdivide(int new_height, int new_width):
    """
    Subdivides image to 2*4 rectangles, and stores the coordinates of the opposite corners of them. 
    These are used to loop through a specific rectangles
    points in the image to convert the values of the rectangle to a braille character
    """
    cdef int y_cord, x_cord
    cdef list grid

    grid = []
    grid_append = grid.append
    for y_cord in range(0, new_height, 4):
        row = [[x_cord, y_cord, x_cord + 2, y_cord + 4] for x_cord in range(0, new_width, 2)]
        grid_append(row)
    return grid


cpdef unicode form_braille(list block, unsigned char[:,:] image):
    """
    Uses the given opposite corners to read the values in the rectangle.
    Forms the final braille character based on the values/statuses.
    """
    cdef int x_1, x_2, y_1, y_2
    cdef int y_block, y_global, x_block, x_global
    cdef int unicode_sum = 10240

    x_1, y_1, x_2, y_2 = block  # The opposite corners

    values = ((1, 2, 4, 64), (8, 16, 32, 128))
    y_block = 0
    x_block = 0
    for y_global in range(y_1, y_2):

        for x_global in range(x_1, x_2):
            if image[y_global, x_global]:
                unicode_sum += values[x_block][y_block]
            x_block += 1
        x_block = 0
        y_block += 1

    return chr(unicode_sum)


cpdef unicode form_string(list grid, unsigned char[:,:] image):
    """Forms the final string by looping through the rectangles by rows."""

    cpdef list frame = []
    cpdef list row, string

    frame_append = frame.append
    convert = form_braille
    for row in grid:
        string = []
        string_append = string.append
        for block in row:
            string_append(convert(block, image))
        frame_append("".join(string))

    return '\n'.join(frame)
