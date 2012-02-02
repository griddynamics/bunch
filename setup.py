#!/usr/bin/env python

import os
import sys
from bunch import version
from setuptools import setup
from string import strip

def get_dependencies():
    with open('dependencies.txt', 'r') as file:
        return map(lambda x: strip(x, ' \n'), file.readlines())

def get_packages():
    packages = []
    for root, dirnames, filenames in os.walk('bunch'):
        if '__init__.py' in filenames:
            packages.append(".".join(os.path.split(root)).strip("."))

    return packages

required_modules = get_dependencies()

setup(name='bunch',
    version=version,
    description='Bunch test organizer for Lettuce',
    author=u'GD',
    author_email='skosyrev@griddynamics.com',
    url='http://github.com/TODO',
    packages=get_packages(),
    install_requires=required_modules,
    entry_points={
        'console_scripts': ['bunch = bunch.cli:main'],
    },
)
  