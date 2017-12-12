from distutils.core import setup
from Cython.Build import cythonize

setup(
    ext_modules=cythonize("src\\util\\solar_angles.pyx"), requires=['Cython', 'pandas']
)
