======
Barril
======


.. image:: https://img.shields.io/pypi/v/barril.svg
    :target: https://pypi.python.org/pypi/barril

.. image:: https://img.shields.io/pypi/pyversions/barril.svg
    :target: https://pypi.org/project/barril

.. image:: https://img.shields.io/travis/ESSS/barril.svg
    :target: https://travis-ci.org/ESSS/barril

.. image:: https://ci.appveyor.com/api/projects/status/2y9spccc6pk9gh96/branch/master?svg=true
    :target: https://ci.appveyor.com/project/ESSS/barril/?branch=master&svg=true

.. image:: https://codecov.io/gh/ESSS/barril/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/ESSS/barril

.. image:: https://img.shields.io/readthedocs/pip.svg
    :target: https://barril.readthedocs.io/en/latest/

What is Barril?
===============

Python package to manage units for physical quantities.

Quick example:

.. code-block:: python

    from barril.units import Scalar

    s1 = Scalar(10, 'm')
    s2 = Scalar(500, 'cm')
    assert s1 + s2 == Scalar(15, 'm')


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

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
.. _`GitHub page` :                   https://github.com/ESSS/barril
.. _Cookiecutter:                     https://github.com/audreyr/cookiecutter
.. _pytest:                           https://github.com/pytest-dev/pytest
.. _tox:                              https://github.com/tox-dev/tox
