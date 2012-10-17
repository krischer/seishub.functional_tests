#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Functional testing for SeisHub.
"""
from setuptools import find_packages, setup
import os


with open(os.path.join("seishub", "functional_tests", "VERSION.txt")) as o_f:
    VERSION = o_f.read()

setup(
    name="seishub.functional_tests",
    version=VERSION,
    description="Functional testing suite for SeisHub.",
    long_description="""
    None yet...
    """,
    author="Lion Krischer",
    author_email="krischer@geophysik.uni-muenchen.de",
    license="GNU Lesser General Public License, Version 3 (LGPLv3)",
    platforms="OS Independent",
    classifiers=[],
    keywords=["SeisHub"],
    packages=find_packages(),
    namespace_packages=["seishub"],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "setuptools",
        "seishub.core"])
