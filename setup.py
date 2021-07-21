# Copyright (C) 2015 - 2019 Red Hat, Inc.
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; If not, see <http://www.gnu.org/licenses/>.
#
# Red Hat Author(s): Anne Mulhern <amulhern@redhat.com>
# Other Author(s): Anne Mulhern <mulhern@cs.wisc.edu>

"""
Python packaging file for setup tools.
"""

# isort: STDLIB
import os

# isort: THIRDPARTY
import setuptools


def local_file(name):
    """
    Function to obtain the relative path of a filename.
    """
    return os.path.relpath(os.path.join(os.path.dirname(__file__), name))


README = local_file("README.rst")

with open(local_file("src/justbases/version.py")) as o:
    exec(o.read())  # pylint: disable=exec-used


with open(local_file("README.rst"), encoding="utf-8") as o:
    long_description = o.read()

setuptools.setup(
    name="justbases",
    version=__version__,  # pylint: disable=undefined-variable
    author="Anne Mulhern",
    author_email="mulhern@cs.wisc.edu",
    description="conversion of ints and rationals to any base",
    long_description=long_description,
    platforms=["Linux"],
    license="LGPLv2+",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU Lesser General Public License v2 or later (LGPLv2+)",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Software Development :: Libraries",
        "Topic :: Scientific/Engineering :: Mathematics",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages("src"),
)
