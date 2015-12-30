#!/usr/bin/python3
# Copyright (c) 2015 Davide Gessa
# Distributed under the MIT software license, see the accompanying
# file COPYING or http://www.opensource.org/licenses/mit-license.php.

from setuptools import find_packages
from setuptools import setup

setup(name='dappforum',
	version='0.1',
	description='DAPP Project for FS',
	author='Emanuele Muggiri',
	author_email='emanuele.mug@gmail.com',
	setup_requires='setuptools',
	package_dir={'':'library'},
	packages=['dappforum']
)
