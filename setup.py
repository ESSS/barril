#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import find_packages, setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['attrs>=18.1.0', 'numpy>=1.11.0']

setup(
    author="ESSS",
    author_email='foss@esss.co',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    description="Python package to manage units for physical quantities",
    extras_require={
        ':python_version == "2.7"': [ 'ruamel.ordereddict>=0.4.6' ],
        'docs': [ 'sphinx >= 1.4', 'sphinx_rtd_theme', 'sphinx-autodoc-typehints'],
        'testing': ['pytest', 'pytest-cov']
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='barril',
    name='barril',
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    url='https://github.com/ESSS/barril',
    use_scm_version=True,
    setup_requires=['setuptools_scm'],
    zip_safe=False,
)
