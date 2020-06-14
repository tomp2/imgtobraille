"""Compile cython modules"""

from setuptools import setup
from Cython.Build import cythonize

setup(
    ext_modules=cythonize("source/*.pyx"),
    zip_safe=False,
)
