1.17.0 (2023-05-02)
-------------------

* Standardize the usage of ``lbmol``
* Add more valid units for ``mole per mass`` category

1.16.0 (2023-04-26)
-------------------

* Add more units for ``mole per mass`` quantity.
* Define a ``molality`` category.

1.15.0 (2023-04-03)
-------------------

* Add ``cubic meter per day per kilogram-force per square centimeter`` (``m3/d/kgf/cm2``) unit to ``productivity index`` category.
* Add gauge pressures units ``Pa(g)``, ``kPa(g)``, ``bar(g)``, and ``kgf/cm2(g)`` to ``pressure`` category.

1.14.1 (2022-11-03)
-------------------

* Add ``mole per mass`` quantity (``mol/kg``).

1.13.0 (2021-11-30)
-------------------

* Update ``Newton second per meter`` unit from ``Ns/m`` to ``N.s/m`` to get unit display consistent with other units in the same category (support for the old unit input added).
* Add ``force per velocity squared`` quantity (``N.s2/m2``, ``lbf.s2/ft2``, ``lbf.s2/in2``, ``kgf.s2/m2``).

1.12.0 (2021-11-08)
-------------------

* ``barril`` is now fully type annotated, being tested with ``mypy``.
* ``Array`` and ``FixedArray`` are ``Generic`` subclasses, parametrized by the container type.

1.11.1 (2021-10-08)
-------------------

* Fixed typos in unit names: ``kilkodynes`` (unit=kdyne) fixed to ``kilodynes``, ``killowatts/cubic metre degree Kelvin`` (unit=kW/m3.K) fixed to ``kilowatts/cubic metre degree Kelvin``.

1.11.0 (2021-06-18)
-------------------

* Add new unit: "Stokes" (``St``).
* Use ``TypeCheckingSupport`` from ``oop-ext 1.1``.
* Add ``cubic feet per day per psi`` (``ft3/psi.d``) unit to ``productivity index`` category.
* Add ``calories/metre hour degree Celsius`` (``cal/m.h.degC``) unit to ``thermal conductivity`` category.
* Add ``calorie/hour square metre deg C`` (``cal/h.m2.degC``) unit to ``heat transfer coefficient`` category.
* Add ``std cubic metres/second`` (``sm3/s``) unit to ``standard volume per time`` category.
* Add ``million std cubic feet/stock tank barrel`` (``MMscf/stb``), ``stock tank barrel/std cubic feet`` (``stb/scf``) and ``stock tank barrel/million std cubic feet`` (``stb/MMscf``) units to ``standard volume per standard volume`` category.

1.10.0 (2020-10-22)
-------------------

* Removing ``thermodynamic temperature`` as default category for ``degF`` and ``degR`` units.

1.9.0 (2020-02-20)
------------------

* New ``classmethod`` ``Array.FromScalars`` that creates an ``Array`` from a ``List[Scalar]``.
* Add new unit: "barrel per second" (``bbl/s``).

1.8.0 (2020-01-10)
------------------

* Add new category: "standard volume per standard volume".
* Move unit ``sm3/sm3`` from "volume per volume" to "standard volume per standard volume".

1.7.2 (2019-10-16)
------------------

* ``_foundation`` has been renamed to ``_util``, and a lot of functions which were not being
  used anymore have been removed.
* Add new unit category mass temperature per mol (``kg.K/mol``).
* Some units have been renamed as they were deemed out-of-place in the oil industry to something more usual (for example, ``1000ft3/d`` became ``Mcf/d``).
  The old representation of those units is still supported, but they will be automatically translated during ``Quantity`` creation, so this change should not affect users much.
* Fix division ``1.0 / a`` where ``a`` is a ``Scalar`` or ``Array`` and also add support for floor
  division, i.e., operations like ``a // b``  where ``a`` and ``b`` are ``Scalar`` or ``Array``
  (and combinations with ``float`` or ``int``).
* Add new unit category for Joule-Thomson coefficient (``K/Pa``).
* Add new temperature unit for density derivative in respect to temperature (``kg/m3.K``).

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
