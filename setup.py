#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

import io
from setuptools import find_packages, setup

with io.open('README.rst', encoding='UTF-8') as readme_file:
    readme = readme_file.read()

with io.open('CHANGELOG.rst', encoding='UTF-8') as changelog_file:
    history = changelog_file.read()

requirements = ['attrs>=18.1.0', 'numpy>=1.11.0']
extras_require = {
    ':python_version == "2.7"': ['ruamel.ordereddict>=0.4.6'],
    'docs': ['sphinx >= 1.4', 'sphinx_rtd_theme', 'sphinx-autodoc-typehints'],
    'testing': ['codecov', 'pytest', 'pytest-cov', 'pytest-mock'],
}

setup(
    author="ESSS",
    author_email='foss@esss.co',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    description="Python package to manage units for physical quantities",
    extras_require=extras_require,
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    python_requires=">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, !=3.5.*",
    keywords='barril',
    name='barril',
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    url='https://github.com/ESSS/barril',
    use_scm_version=True,
    setup_requires=['setuptools_scm'],
    zip_safe=False,
)
