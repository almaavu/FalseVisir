#!/usr/bin/env python3

from setuptools import setup, find_packages
import os
import sys


    
setup(
    name='falsevisir',
    version='1.0.0',
    url='https://github.com/almaavu/falsevisir/',
    author='ffsedd',
    author_email='ffsedd@gmail.com',
    description='Combine IR and VIS image to FALSE COLOR',
    packages=find_packages(where=''),  # Required
    #scripts=['qq'],
    install_requires=['numpy', 'matplotlib', 'imageio', 'scikit-image'],
    include_package_data=True,
)
