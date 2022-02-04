# -*- coding: utf-8 -*-
"""
Created on Fri Feb  4 09:17:50 2022

@author: olehe
"""

import pathlib
from setuptools import setup, find_packages

HERE = pathlib.Path(__file__).parent

VERSION = '0.1.0'
PACKAGE_NAME = 'GrooveGenerator'
AUTHOR = 'Ole Adrian Heggli'
AUTHOR_EMAIL = 'oleheggli@gmail.com'
URL = 'TOBEINSERTED'

LICENSE = 'MIT License'
DESCRIPTION = 'Collection of functions to generate and analyse rhythm patterns.'
LONG_DESCRIPTION = (HERE / "README.md").read_text()
LONG_DESC_TYPE = "text/markdown"

INSTALL_REQUIRES = [
      'numpy',
      'pandas',
	  'mido',
	  'scipy'
]

setup(name=PACKAGE_NAME,
      version=VERSION,
      description=DESCRIPTION,
      long_description=LONG_DESCRIPTION,
      long_description_content_type=LONG_DESC_TYPE,
      author=AUTHOR,
      license=LICENSE,
      author_email=AUTHOR_EMAIL,
      url=URL,
      install_requires=INSTALL_REQUIRES,
      packages=find_packages()
      )
