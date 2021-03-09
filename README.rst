======
Barril
======


.. image:: https://img.shields.io/pypi/v/barril.svg
    :target: https://pypi.python.org/pypi/barril

.. image:: https://img.shields.io/pypi/pyversions/barril.svg
    :target: https://pypi.org/project/barril

.. image:: https://github.com/ESSS/barril/workflows/build/badge.svg
    :target: https://github.com/ESSS/barril/actions

.. image:: https://codecov.io/gh/ESSS/barril/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/ESSS/barril

.. image:: https://img.shields.io/readthedocs/barril.svg
    :target: https://barril.readthedocs.io/en/latest/

What is Barril?
===============

Python package to manage units for physical quantities.

Quick example:

.. code-block:: python

    from barril.units import Scalar

    s1 = Scalar(10, "m")
    s2 = Scalar(500, "cm")
    assert s1 + s2 == Scalar(15, "m")


Features
--------

* Pre-defined unit database containing several physical quantities for the Oil & Gas industry.
* Data types with an associated unit: ``Scalar``, ``Array``, ``Quantity``, ``FixedArray``.
* Automatic conversion during arithmetic operations.

Development
-----------

For complete description of what type of contributions are possible,
see the full `CONTRIBUTING <CONTRIBUTING.rst>`_ guide.

Here is a quick summary of the steps necessary to setup your environment to contribute to ``barril``.

#. Create a virtual environment and activate it::

    $ python -m virtualenv .env
    $ .env\Scripts\activate  # windows
    $ source .env/bin/activate  # linux


   .. note::

       If you use ``conda``, you can install ``virtualenv`` in the root environment::

           $ conda install -n root virtualenv

       Don't worry as this is safe to do.

#. Update ``pip``::

    $ python -m pip install -U pip

#. Install development dependencies::

    $ pip install -e .[testing]

#. Install pre-commit::

    $ pre-commit install

#. Run tests::

    $ pytest --pyargs barril

#. Generate docs locally::

    $ tox -e docs

   The documentation files will be generated in ``docs/_build``.

Release
-------

A reminder for the maintainers on how to make a new release.

Note that the VERSION should folow the semantic versioning as X.Y.Z
Ex.: v1.0.5

1. Create a ``release-VERSION`` branch from ``upstream/master``.
2. Update ``CHANGELOG.rst``.
3. Push a branch with the changes.
4. Once all builds pass, push a ``VERSION`` tag to ``upstream``.
5. Merge the PR.

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
.. _`GitHub page` :                   https://github.com/ESSS/barril
.. _Cookiecutter:                     https://github.com/audreyr/cookiecutter
.. _pytest:                           https://github.com/pytest-dev/pytest
.. _tox:                              https://github.com/tox-dev/tox
