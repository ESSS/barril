#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""The setup script."""
import io

from setuptools import find_packages
from setuptools import setup

with io.open("README.rst", encoding="UTF-8") as readme_file:
    readme = readme_file.read()

with io.open("CHANGELOG.rst", encoding="UTF-8") as changelog_file:
    history = changelog_file.read()

requirements = ["attrs>=18.1.0", "numpy>=1.11.0", "oop-ext>=1.1"]
extras_require = {
    "docs": ["sphinx >= 1.4", "sphinx_rtd_theme", "sphinx-autodoc-typehints", "typing_extensions"],
    "testing": [
        "codecov",
        "data-science-types",
        "mypy",
        "pre-commit",
        "pytest",
        "pytest-cov",
        "pytest-mock",
        "tox",
    ],
}

setup(
    author="ESSS",
    author_email="foss@esss.co",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    description="Python package to manage units for physical quantities",
    extras_require=extras_require,
    install_requires=requirements,
    license="MIT license",
    long_description=readme + "\n\n" + history,
    include_package_data=True,
    python_requires=">=3.6",
    keywords="barril",
    name="barril",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    url="https://github.com/ESSS/barril",
    use_scm_version=True,
    setup_requires=["setuptools_scm"],
    zip_safe=False,
)
