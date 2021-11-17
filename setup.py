#!/usr/bin/env python3
'''
Setup script for the package. Just use 'python setup.py install' to install
'''
from setuptools import setup

setup(
    name='demo',
    packages=['demo'],
    include_package_data=True,
    install_requires=[
        'flask',
        'flask_sqlalchemy',
        'flask-wtf',
        'wtforms',
        'flask_bcrypt',
        'flask_login'
    ],
)
