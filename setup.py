#!/usr/bin/env python

import os
import sys
from lettuce_bunch import version
from setuptools import setup
from string import strip

def get_dependencies():
    with open('dependencies.txt', 'r') as file:
        return map(lambda x: strip(x, ' \n'), file.readlines())

"""
def get_packages():
    packages = []
    for root, dirnames, filenames in os.walk('lettuce_bunch'):
        if '__init__.py' in filenames:
            packages.append(".".join(os.path.split(root)).strip("."))

    return packages
"""

def get_packages(package):
    """
    Return root package and all sub-packages.
    """
    return [dirpath
            for dirpath, dirnames, filenames in os.walk(package)
            if os.path.exists(os.path.join(dirpath, '__init__.py'))]

def get_package_data(package):
    """
    Return all files under the root package, that are not in a
    package themselves.
    """
    walk = [(dirpath.replace(package + os.sep, '', 1), filenames)
            for dirpath, dirnames, filenames in os.walk(package)
            if not os.path.exists(os.path.join(dirpath, '__init__.py'))]

    filepaths = []
    for base, filenames in walk:
        filepaths.extend([os.path.join(base, filename)
                          for filename in filenames])
    return {package: filepaths}


#required_modules = get_dependencies()
required_modules = ['lettuce', 'jinja2', 'PyYAML', 'nose', 'anyjson', 'lxml']
package='lettuce_bunch'

license = 'GPL v3.0+'
setup(name='lettuce-bunch',
    version=version,
    description='Bunch test organizer for Lettuce',
    author=u'GD',
    author_email='skosyrev@griddynamics.com',
    url='http://github.com/TODO',
    packages=get_packages(package),
    package_data=get_package_data(package),
    license=license,
    install_requires=required_modules,
    entry_points={
        'console_scripts': ['bunch = lettuce_bunch.cli:main'],
    },
)
  
