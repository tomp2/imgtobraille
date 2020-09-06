"""Dithering algorithms to binarize the images."""

import random as rnd
import numpy as np
import random as rnd

import numpy as np

cpdef unsigned char[:,:] threshold(int h, int w, unsigned char[:,:] img):
    """Threshing/average dithering."""
    cdef int x, y, value, out

    for y in range(h):
        for x in range(w):
            value = img[y, x]
            if value > 80:
                out = 1
            else:
                out = 0
            img[y, x] = out
    return img


cpdef unsigned char[:,:] quantize(int h, int w, unsigned char[:,:] img):
    """Floyd–Steinberg dithering."""

    cpdef int x, y, old_pixel, new_pixel
    cpdef double quant_error
    cpdef int average = np.average(img)

    # Update res to allow dithering to function better near the borders
    img = np.pad(img, 1)

    for y in range(1, h):
        for x in range(1, w):
            old_pixel = img[y, x]
            new_pixel = 255 if old_pixel > average else 0
            img[y, x] = new_pixel

            quant_error = old_pixel - new_pixel
            quant_error = 0 if quant_error < 0 else quant_error * 0.5

            img[y, x + 1] += int(quant_error * 7 / 16)
            img[y + 1, x - 1] += int(quant_error * 3 / 16)
            img[y + 1, x] += int(quant_error * 5 / 16)
            img[y + 1, x + 1] += int(quant_error * 1 / 16)


    return img[1:-1,1:-1]


cpdef unsigned char[:,:] random(int h, int w, unsigned char[:,:] img):
    """Random dithering."""

    cpdef int x, y, value, out
    cdef float change

    for y in range(h):
        for x in range(w):
            value = img[y, x]

            if value > 240:
                continue
            elif value < 80:
                out = 0
            else:
                value -= 127
                chance = (value - 127) ** 3 / 20000 + 50    # Customizable
                out = 1 if chance > rnd.random() else 0
            img[y, x] = out
    return img
