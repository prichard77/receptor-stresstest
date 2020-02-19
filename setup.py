#!/usr/bin/env python

# Copyright (c) 2020 Red Hat, Inc.
# All Rights Reserved.

from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="receptor-stresstest",
    version="1.0.0",
    author="jag",
    url="https://github.com/project-receptor/receptor-stresstest",
    license="GPLv3",
    packages=find_packages(),
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[],
    zip_safe=False,
    entry_points={"receptor.worker": "receptor_stresstest = receptor_stresstest.worker",},
    classifiers=["Programming Language :: Python :: 3",],
    extras_require={"dev": ["pytest", "flake8", "pylint", "black"]},
)
