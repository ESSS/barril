from setuptools import find_packages
from setuptools import setup

with open("README.rst", encoding="UTF-8") as readme_file:
    readme = readme_file.read()

with open("CHANGELOG.rst", encoding="UTF-8") as changelog_file:
    history = changelog_file.read()

requirements = ["attrs>=18.1.0", "numpy>=1.11.0", "oop-ext>=1.1", "typing_extensions"]
extras_require = {
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
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
    ],
    description="Python package to manage units for physical quantities",
    extras_require=extras_require,
    install_requires=requirements,
    license="MIT license",
    long_description=readme + "\n\n" + history,
    long_description_content_type="text/x-rst",
    include_package_data=True,
    python_requires=">=3.9",
    keywords="barril",
    name="barril",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    url="https://github.com/ESSS/barril",
    zip_safe=False,
)
