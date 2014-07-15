#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name = "test-out",
    version = "0.1.3",
    description = "Python class to provide helpful logging, test run data and summary statistics for automated tests.",
    author = "Richard Pappalardo",
    author_email = "rpappalax@gmail.com",
    url = "https://github.com/rpappalax/test-out",
    install_requires = [],
    packages = find_packages(),
    keywords = ['testing', 'logging', 'reporting', 'stats'],
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        ]
    )
