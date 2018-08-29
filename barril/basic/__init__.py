from __future__ import unicode_literals

from ._closing import Closing
from ._expression_check import CheckExpressionSymbols, GetExpressionSymbols
from ._import_module import ImportModule, ImportToken
from ._native_algorithms import (
    AsList, Flatten, Intersection, IterFlattened, ListDuplicates, MergeDictsRecursively,
    OrderedIntersection, RemoveDuplicates)
from ._two_way_dict import TwoWayDict

'''
Basic extensions to the python language or standard library.

As a rule of thumb, objects and functions here shouldn't depend on any other modules on COI-lib.
'''
