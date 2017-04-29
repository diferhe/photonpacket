from setuptools import setup
from Cython.Build import cythonize
from setuptools.extension import Extension
import numpy

extensions = [
        Extension('photonpacket.frameutils.coinc',['photonpacket/frameutils/coinc.pyx']),
        Extension('photonpacket.frameutils.arraysplit',['photonpacket/frameutils/arraysplit.pyx'])
        ]

setup(
    ext_modules=cythonize(extensions),
    include_dirs=[numpy.get_include()]
)