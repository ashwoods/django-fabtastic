#!/usr/bin/env python
from setuptools import setup, find_packages

#open version file
#this file is generated automatically with a pre-commit script
VERSION = open('VERSION').read().lstrip('version: ').rstrip('\n')


setup(name='fabtastic',
      version = '0.0.1',
      packages=find_packages(),
      exclude_package_data={'fabtastic': ['bin/*.pyc']},
      setup_requires = ["setuptools_git >= 0.3",'fabric'],
      #scripts
      )
