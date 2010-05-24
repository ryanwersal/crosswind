#!/usr/bin/env python3

classifiers = [
"Development Status :: 3 - Alpha",
"Environment :: Console",
"Intended Audience :: Developers",
"License :: OSI Approved :: Apache Software License",
"Operating System :: OS Independent",
"Programming Language :: Python :: 3",
"Topic :: Software Development :: Code Generators",
"Topic :: Software Development :: Libraries :: Python Modules",
]

from distutils.core import setup

setup(
   name="3to2_py3k",
   packages=["lib3to2","lib3to2.fixes","lib3to2.tests"],
   scripts=["3to2"],
   version="0.1a4",
   url="http://www.startcodon.com/wordpress/?cat=8",
   author="Joe Amenta",
   author_email="amentajo@msu.edu",
   classifiers=classifiers,
   description="Refactors valid 3.x syntax into valid 2.x syntax, if a syntactical conversion is possible",
   long_description="",
   license="",
   platforms="",
)
