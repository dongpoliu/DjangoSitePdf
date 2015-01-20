#!/usr/bin/env python

from setuptools import setup, find_packages

VERSION = __import__('DjangoSitePdf').__version__


setup(name='DjangoSitePdf',
      version='0.1',
      description='A Django Site for Chinese Picture-book (PDF), this is an updated version of codester',
      author='DongpoLiu',
      author_email='rubinliu@hotmailmail.com',
      url='https://github.com/dongpoliu/DjangoSitePdf.git',
      packages=find_packages(),
      classifiers = [
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Framework :: Django",
    ],
    include_package_data = True,
    zip_safe = False,
    install_requires = ['django', 'rest_framework',]
)
