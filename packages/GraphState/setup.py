#!/usr/bin/python
# -*- coding: utf8
from distutils.core import setup

setup(
    name='GraphState',
    version='0.0.2',
    author='S. Novikov',
    author_email='dr.snov@gmail.com',
    packages=['nickel', 'nickel.test', 'graph_state', 'graph_state.test'],
    url='http://pypi.python.org/pypi/GraphState/',
    license='LICENSE.txt',
    description='Generalization of B.G.Nickel et al algorithm for identifying graphs',
    long_description=open('README.txt').read(),
)