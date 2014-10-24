#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import massproxy

APP_NAME = 'massproxy'

settings = dict()


# Publish Helper.
if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

settings.update(
    name=APP_NAME,
    version=massproxy.__version__,
    description='Mass proxy crawler from public internet.',
    long_description=open('README.md').read(),  # + '\n\n' +
    #open('HISTORY.rst').read(),
    author=massproxy.__author__,
    url='https://github.com/requests/massproxy',
    packages=['massproxy', ],
    install_requires=['requests>=2.0.0', 'BeautifulSoup4>=4.0.0'],
    extras_require={'rsa': ['requests>=2.0.0', 'BeautifulSoup4>=4.0.0']},
    license=massproxy.__license__,
    classifiers=(
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ),
    zip_safe=False,
    tests_require=['mock'],
    test_suite='tests'
)

setup(**settings)
