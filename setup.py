from distutils.core import setup, Extension
from Cython.Build import cythonize

ext_modules = [
    Extension('main', ['main.pyx']),
    Extension('entities', ['entities.pyx'])
]

setup(ext_modules=cythonize(ext_modules))
