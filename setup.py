#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

tests_requirements = ['requests', 'PyYAML']

setup(name='enzyme',
    version='0.4.2-dev',
    license='Apache 2.0',
    description='Python video metadata parser',
    long_description=open('README.rst').read() + '\n\n' + open('HISTORY.rst').read(),
    keywords='parser video metadata mkv',
    url='https://github.com/Diaoul/enzyme',
    author='Antoine Bertin',
    author_email='diaoulael@gmail.com',
    packages=find_packages(),
    package_data={'enzyme.parsers.ebml': ['specs/matroska.xml'], 'enzyme.tests': ['parsers/ebml/test1.mkv.yml']},
    classifiers=['Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Topic :: Multimedia :: Video',
        'Topic :: Software Development :: Libraries :: Python Modules'],
    python_requires="<3.12,>=3.8",
    test_suite='enzyme.tests.suite',
    tests_require=tests_requirements,
    extras_require={'test': tests_requirements})
