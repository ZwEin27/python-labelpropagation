from distutils.core import setup
from setuptools import Extension,find_packages
from os import path

setup(
    name = 'labelprop',
    version = '0.1.3',
    description = 'Python implementation of label propagation',
    author = 'Lingzhe Teng',
    author_email = 'zwein27@gmail.com',
    url = 'https://github.com/ZwEin27/python-labelpropagation',
    download_url = 'https://github.com/ZwEin27/python-labelpropagation/tarball/0.1.3',
    packages = find_packages(),
    keywords = ['label propagation', 'label', 'propagation', 'labelpropagation']
)