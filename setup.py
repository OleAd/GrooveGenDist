# -*- coding: utf-8 -*-
"""
Created on Fri Feb  4 09:17:50 2022

@author: olehe
"""

import pathlib
from setuptools import setup, find_packages

HERE = pathlib.Path(__file__).parent

VERSION = '0.1.3'
PACKAGE_NAME = 'groovegenerator'
AUTHOR = 'Ole Adrian Heggli'
AUTHOR_EMAIL = 'oleheggli@gmail.com'
URL = 'https://github.com/OleAd/GrooveGenDist/'

LICENSE = 'MIT License'
DESCRIPTION = 'Collection of functions to generate and analyse rhythm patterns.'
LONG_DESCRIPTION = (HERE / "README.md").read_text()
LONG_DESC_TYPE = "text/markdown"

INSTALL_REQUIRES = [
      'numpy>=1.21.2',
      'pandas>=1.3.3',
	  'mido>=1.2.10',
	  'scipy>=1.7.1'
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
      packages=find_packages(),
	  include_package_data=True,
	  package_data={'': ['samples/*.wav']}
      )
