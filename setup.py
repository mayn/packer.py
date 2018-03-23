from distutils.core import setup
from setuptools import find_packages

setup(
    name='packer.py',
    version='0.1.0',
    author='Matthew Aynalem',
    author_email='maynalem@gmail.com',
    packages=find_packages('packerpy'),
    url='https://github.com/mayn/packer.py',
    license='Apache License 2.0',
    description='packer.py - python library for interacting with hashicorp packer CLI',
    keywords="hashicorp packer",
    long_description=open('README.rst').read(),
    install_requires=[
    ],
    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)
