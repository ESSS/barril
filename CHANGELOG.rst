UNRELEASED
----------

* ``_foundation`` has been renamed to ``_util``, and a lot of functions which were not being
  used anymore have been removed.
* Add new unit category mass temperature per mol (``kg.K/mol``).
* Some units have been renamed as they were deemed out-of-place in the oil industry to something more usual (for example, ``1000ft3/d`` became ``Mcf/d``).
  The old representation of those units is still supported, but they will be automatically translated during ``Quantity`` creation, so this change should not affect users much.

1.7.1 (2019-10-03)
------------------

* Fixed bug in ``/`` and ``-`` operators for ``FixedArray``.

1.7.0 (2019-06-18)
------------------

* Add unit system.

1.6.1 (2019-04-11)
------------------

* Change export to include ICurve and Curve and exclude IReadOnlyScalar.

1.6.0 (2019-04-10)
------------------

* Add curve implementation.
* Add support to interfaces from oop-ext.
* Drop support to Python 2.

1.5.0 (2019-01-09)
------------------

* ``Quantity.CheckValue`` now raises ``QuantityValidationError`` instead of ``ValueError``.

1.4.0 (2018-12-17)
------------------

* Add new category for "concentration ratio".

1.3.0 (2018-10-13)
------------------

* Add "per micrometre" unit to "per length" category.
* Remove internal ``barril.fixtures``  module as it is not necessary or part of the public API.

1.2.0 (2018-09-26)
------------------

* Add units for defining Spring-Dashpot movements.

1.1.0 (2018-09-24)
------------------

* Add ``number`` and ``fraction`` properties to ``FractionValue``.
* Add ``unit`` read-only property to ``Quantity``.


1.0.0 (2018-09-21)
------------------

* First feature release.

0.1.0 (2018-09-03)
------------------

* First release on PyPI.
