#!/usr/bin/python
# -*- coding: utf-8 -*-

from distutils.core import setup

with open('README.md') as file:
    long_description = file.read()

__version__ = '0.0.1'

setup(
    name='test',
    version=__version__,
    long_description=long_description,
    description='Interesting ways of mixing human collaboration with Machine Learning.',
    url='http://www.github.com/rfaulkner/test',
    author="Ryan Faulkner",
    author_email="bobs.ur.uncle@gmail.com",
    packages=['test.src', 'test.config'],
    install_requires=[
        'Flask == 0.9',
        'python-dateutil >= 2.1',
        'numpy >= 1.8.0',
        'theano >= 0.6.0rc1',
        # MySQLdb is not in PyPi
    ],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    data_files=[('readme', ['README.md'])]
)
