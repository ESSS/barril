from __future__ import absolute_import, unicode_literals

import numpy
from six.moves import zip  # @UnresolvedImport


#===================================================================================================
# _ValueGenerator
#===================================================================================================
class _ValueGenerator(object):
    '''
    Generator for values so that 1 one of the values is generated from iterating through a list and
    the other is a fixed values returned.

    Special case is if a numpy array is found... if it is, just yields the numpy array all at once
    (as it's able to make the whole range of operations without the need for an iteration in the
    python side).

    Internal API used to convert array values.
    '''

    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2

        self.iterate_1st = isinstance(p1, (tuple, list))
        self.iterate_2nd = isinstance(p2, (tuple, list))

    def IsNumpy(self):
        '''
        :rtype: bool
        :returns:
            If either one of the contained elements is a numpy array.
        '''
        return isinstance(self.p1, numpy.ndarray) or isinstance(self.p2, numpy.ndarray)

    def IsTuple(self):
        '''
        :rtype: bool
        :returns:
            Whether the element(s) iterated is a tuple.
        '''
        if self.iterate_1st and self.iterate_2nd:
            return isinstance(self.p1, tuple) and isinstance(self.p2, tuple)

        if self.iterate_1st:
            return isinstance(self.p1, tuple)

        if self.iterate_2nd:
            return isinstance(self.p2, tuple)

        return False

    def __iter__(self):
        '''
        Yield the individual values we should convert (which may mean the same number all the time
        and the value being iterated in a list). Numpy is a special case (see classdocs)
        '''
        if self.IsNumpy():
            yield self.p1, self.p2

        elif self.iterate_1st and not self.iterate_2nd:
            static_value = self.p2
            for v in self.p1:
                yield static_value, v

        elif not self.iterate_1st and self.iterate_2nd:
            static_value = self.p1
            for v in self.p2:
                yield v, static_value

        elif not self.iterate_1st and not self.iterate_2nd:
            yield self.p1, self.p2

        else:  # iterate both
            for v0, v1 in zip(self.p1, self.p2):
                yield v0, v1
