#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
 Modbus TCP: Implementation of Modbus TCP/IP protocol in python

 (C)2014 - Rasmus Letterkrantz - Rasmus.Letterkrantz@gmail.com

 This is distributed under the MIT license (MIT), see LICENSE.txt
"""

from setuptools import setup


version = '0.1'

setup(name='modbus_tcp',
    version=version,
    description="Python module for communicating Modbus Tcp/Ip with a PLC",
    long_description="""
    Provides an easy to use and lightweight module for talking Modbus Tcp/Ip with slave PLC.
    Limited functions are currently implemented!
    """,
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: MIT or The MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Communications',
        'Topic :: Software Development'
    ],
    keywords='modbus, tcp',
    author='Rasmus Letterkrantz',
    author_email='Rasmus.Letterkrantz@gmail.com',
    maintainer='Rasmus Letterkrantz',
    maintainer_email='Rasmus.Letterkrantz@gmail.com',
    url='https://github.com/letterix/modbus-tcp',
    license='MIT',
    packages=['modbus_tcp'],
    platforms=["Linux", "Mac OS X", "Win"],
    )