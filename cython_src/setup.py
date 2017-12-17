from distutils.core import setup
from Cython.Build import cythonize
import numpy

setup(
    ext_modules=cythonize(["cython_src/power_generators.pyx", "cython_src/loads.pyx", "cython_src/house.pyx"]),
    include_dirs=[numpy.get_include()], requires=['numpy', 'pandas']
)