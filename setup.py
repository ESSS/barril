import setuptools

setuptools.setup(
    name="barril",
    version="0.1",
    url="http://github.com/ESSS/barril",
    author='ESSS',
    author_email='foss@esss.co',
    license = 'MIT',
    description="Python package to manage units for physical quantities",
    packages=setuptools.find_packages(),
    install_requires=[],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)