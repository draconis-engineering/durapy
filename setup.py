# setup.py

import os
import sys

from setuptools import Extension, setup

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

try:
    import pybind11

    include_dirs = [pybind11.get_include()]
except ImportError:
    include_dirs = []

if sys.platform == "win32":
    extra_compile_args = ["/O2", "/std:c++17"]
else:
    extra_compile_args = ["-O3", "-std=c++17"]

# Points precisely to the C++ code inside durapy
cpp_source_path = os.path.join("src", "durapy", "maxcompute", "maxcompute.cpp")

ext_modules = [
    Extension(
        name="durapy.unimath._maxcompute",
        sources=[cpp_source_path],
        include_dirs=include_dirs,
        extra_compile_args=extra_compile_args,
        language="c++",
    ),
]

setup(ext_modules=ext_modules)
