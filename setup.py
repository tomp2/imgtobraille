from setuptools import setup
from Cython.Build import cythonize

setup(
    ext_modules=cythonize("program/cython_module.pyx"),
    zip_safe=False,
)