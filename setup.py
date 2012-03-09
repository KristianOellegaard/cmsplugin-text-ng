# coding: utf-8
import os

from setuptools import setup, find_packages
from cmsplugin_text_ng import __version__ as version

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = 'cmsplugin-text-ng',
    version = version,
    description = read('README.rst'),
    author = 'Kristian Øllegaard',
    author_email = 'kristian@oellegaard.com',
    url = 'https://github.com/KristianOellegaard/cmsplugin-text-ng',
    packages = find_packages(),
    zip_safe=False,
    include_package_data = True,
    install_requires=[
        'Django>=1.2',
        'django-cms>=2.0',
        ],
    classifiers = [
        "Development Status :: 3 - Alpha",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        ]
)