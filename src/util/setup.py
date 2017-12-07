from distutils.core import setup
from Cython.Build import cythonize

setup(
    ext_modules=cythonize("/Users/bokleynen/Documents/2Bir/P&O3/Smart-Energy-Home/src/util/solar_angles.pyx"), requires=['Cython', 'pandas']
)
