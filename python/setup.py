#!/usr/bin/env python

from setuptools import setup, find_packages

with open('../README.rst') as f:
    readme = f.read()

with open('../LICENSE') as f:
    license = f.read()

setup(
    name='ShamirSecretSharing',
    version='1.0.0',
    description="Implementation of Shamir's Secret Sharing Algorithm",
    long_description=readme,
    author='Mohamed A. Bamakhrama',
    author_email='mohamed@alumni.tum.de',
    url='https://github.com/mohamed/ShamirSecretSharing',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)
