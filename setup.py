#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup
from JSONLibrary.version import VERSION

requirements = [
    'tox',
    'coverage',
    'robotframework>=3.0',
    'jsonpath-rw==1.4.0'
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='robotframework-jsonlibrary',
    version=VERSION,
    description="robotframework json jsonpath",
    author="Traitanit Huangsri",
    author_email='traitanit.hua@ascendcorp.com',
    url='git@github.com:nottyo/robotframework-jsonlibrary.git',
    packages=[
        'JSONLibrary'
    ],
    package_dir={'robotframework-jsonlibrary':
                 'JSONLibrary'},
    include_package_data=True,
    install_requires=requirements,
    zip_safe=False,
    keywords='robotframework-jsonlibrary',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: QA',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
