#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup
from JSONLibrary.version import VERSION

requirements = [
    'tox',
    'coverage',
    'robotframework>=3.0',
    'jsonpath-rw==1.4.0',
    'jsonpath-rw-ext>=0.1.9'
]

test_requirements = [
    # TODO: put package test requirements here
]


CLASSIFIERS = """
Development Status :: 5 - Production/Stable
License :: Public Domain
Operating System :: OS Independent
Programming Language :: Python
Topic :: Software Development :: Testing
"""[1:-1]

setup(
    name='robotframework-jsonlibrary',
    version=VERSION,
    description="robotframework-jsonlibrary is a Robot Framework test library for manipulating JSON Object. You can manipulate your JSON object using JSONPath",
    author="Traitanit Huangsri",
    author_email='traitanit.hua@gmail.com',
    url='https://github.com/nottyo/robotframework-jsonlibrary.git',
    packages=[
        'JSONLibrary'
    ],
    package_dir={'robotframework-jsonlibrary':
                 'JSONLibrary'},
    include_package_data=True,
    install_requires=requirements,
    zip_safe=False,
    keywords='robotframework-jsonlibrary',
    classifiers=CLASSIFIERS.splitlines(),
    test_suite='tests',
    tests_require=test_requirements
)
