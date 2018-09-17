from __future__ import unicode_literals

from barril._foundation.klass import AllBasesNames, IsInstance, IsSubclass


class _A(object):
    pass


class _B(object):
    pass


class _C(_B):
    pass


class _D(_C, _A):
    pass


class _E(_D, _C, _A):
    pass


def testIsInstance():
    assert IsInstance(_C(), '_B')
    assert IsInstance(_C(), ('_B',))
    assert not IsInstance(_C(), ('_A',))
    assert IsInstance(_C(), ('_A', '_B'))
    assert not IsInstance(_C(), ('_A', '_D'))


def testIsSubclass():
    assert IsSubclass(_C, ('_C',))
    assert IsSubclass(_C, (_C.__name__,))
    assert IsSubclass(_C, '_B')
    assert IsSubclass(_C, _B.__name__)
    assert IsSubclass(_C, ('_B',))
    assert IsSubclass(_C, (_B.__name__,))
    assert not IsSubclass(_C, ('_A',))
    assert not IsSubclass(_C, (_A.__name__,))
    assert IsSubclass(_C, ('_A', '_B'))
    assert not IsSubclass(_C, ('_A', '_D'))
    assert not IsSubclass(_A, ('_C',))


def testKlass():

    class A(object):
        pass

    class B(A):
        pass

    class C(B):
        pass

    class D(C):
        pass

    class Alpha(object):
        pass

    class AlphaC(Alpha, C):
        pass

    assert set(AllBasesNames(A)) == {'object'}
    assert set(AllBasesNames(B)) == {'A', 'object'}
    assert set(AllBasesNames(C)) == {'B', 'A', 'object'}
    assert set(AllBasesNames(D)) == {'C', 'B', 'A', 'object'}
    assert set(AllBasesNames(AlphaC)) == {'Alpha', 'object', 'C', 'B', 'A'}

    assert IsInstance(A(), 'object')
    assert IsInstance(A(), 'A')
    assert IsInstance(B(), 'object')
    assert IsInstance(B(), 'A')
    assert IsInstance(B(), 'B')
    assert IsInstance(C(), 'object')
    assert IsInstance(C(), 'A')
    assert IsInstance(C(), 'B')
    assert IsInstance(C(), 'C')
    assert IsInstance(AlphaC(), 'object')
    assert IsInstance(AlphaC(), 'A')
    assert IsInstance(AlphaC(), A)
    assert IsInstance(AlphaC(), 'B')
    assert IsInstance(AlphaC(), 'C')
    assert IsInstance(AlphaC(), 'Alpha')
    assert IsInstance(AlphaC(), 'AlphaC')
    assert IsInstance(AlphaC(), AlphaC)

    assert not IsInstance(AlphaC(), 'Rubles')
    assert not IsInstance(A(), 'B')
    assert not IsInstance(B(), 'C')


