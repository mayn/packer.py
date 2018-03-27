"""
Copyright 2018 Matthew Aynalem

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
from distutils.core import setup
from setuptools import find_packages

setup(
    name='packer.py',
    version='0.2.0',
    author='Matthew Aynalem',
    author_email='maynalem@gmail.com',
    packages=['packerpy'],
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
