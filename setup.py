#!/usr/bin/env python

from setuptools import setup, find_packages

setup(name='SMBEdit',
      version='0.1.8',
      description='StarMade Blueprint Editor',
      author='Peter Hofmann',
      author_email='',
      url='https://github.com/p-hofmann/SMBEdit',
      packages=find_packages(exclude=('unittests',)),
      entry_points = {
          'console_scripts': [
              'smbedit = smbedit.smbedit:main',
          ],
      },
     )