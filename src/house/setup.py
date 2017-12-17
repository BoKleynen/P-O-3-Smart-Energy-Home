from distutils.core import setup
from Cython.Build import cythonize
import numpy

setup(
    ext_modules=cythonize(["src/house/power_generators.pyx", "src/house/loads.pyx"]),
    include_dirs=[numpy.get_include()]
)