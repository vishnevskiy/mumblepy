# coding=utf-8

from setuptools import setup, find_packages

DESCRIPTION = 'Python Mumble for Humans™'

with open('README.md') as f:
    LONG_DESCRIPTION = f.read()

VERSION = '0.1.0'

setup(
    name='mumble',
    version=VERSION,
    packages=find_packages(),
    author='Stanislav Vishnevskiy',
    author_email='vishnevskiy@gmail.com',
    url='https://github.com/vishnevskiy/mumblepy',
    license='MIT',
    include_package_data=True,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    install_requires=[],
    platforms=['any'],
    classifiers=[],
    test_suite='tests',
)
