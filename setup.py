"""Compile cython modules"""

from setuptools import setup
from Cython.Build import cythonize


setup(name='imgtobraille',
      version='0.1',
      description='Converts images to braille unicode characters',
      url='https://github.com/Kamaleen0/imgtobraille',
      author=' Kamaleen',
      ext_modules=cythonize("imgtobraille/*.pyx"),
      zip_safe=False,
      license='MIT',
      packages=['imgtobraille'],
      install_requires=[
          'natsort',
          'tqdm',
          'pip',
          'python',
          'opencv',
          'cython'
      ]
      )
