from Cython.Build import cythonize
from setuptools import setup

setup(
    ext_modules=cythonize("program/cython_module.pyx"),
    zip_safe=False,
)
