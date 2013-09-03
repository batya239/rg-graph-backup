#!/usr/bin/python
# -*- coding: utf8
from distutils.core import setup

setup(
    name='MincerAdapter',
    version='0.0.1',
    author='D. Batkovich',
    author_email='batya239@gmail.com',
    packages=['mincer_adapter'],
    package_data={'mincer_adapter': ['lib/*.h']},
    url='http://pypi.python.org/pypi/MincerAdapter/',
    license='LICENSE.txt',
    description='Mincer adapter for Python',
    long_description=open('README.txt').read(),
)
