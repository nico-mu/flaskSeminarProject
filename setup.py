'''
Setup script for the package.
'''
from setuptools import setup

setup(
    name='flaskDemo',
    packages=['flaskDemo'],
    include_package_data=True,
    install_requires=[
        'flask'
    ],
)
