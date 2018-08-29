from __future__ import unicode_literals

import pytest

from ben10.foundation.callback import After
from ben10.foundation.decorators import Override
from ben10.foundation.singleton import (
    PushPopSingletonError, Singleton, SingletonAlreadySetError, SingletonNotSetError)


#===================================================================================================
# Test
#===================================================================================================
class Test(object):

    def _TestCurrentSingleton(self, singleton_class, value):
        singleton = singleton_class.GetSingleton()
        assert singleton.value == value

    def testSingleton(self):

        class MySingleton(Singleton):

            def __init__(self, value):
                self.value = value

            @classmethod
            @Override(Singleton.CreateDefaultSingleton)
            def CreateDefaultSingleton(cls):
                return MySingleton(value=0)

        # Default singleton (created automatically and also put in the stack)
        self._TestCurrentSingleton(MySingleton, 0)
        default_singleton = MySingleton.GetSingleton()
        default_singleton.value = 10

        # SetSingleton must be called only when there is no singleton set. In this case,
        # GetSingleton already set the singleton.
        with pytest.raises(SingletonAlreadySetError):
            MySingleton.SetSingleton(MySingleton(value=999))
        self._TestCurrentSingleton(MySingleton, 10)

        # push a new instance and test it
        MySingleton.PushSingleton(MySingleton(2000))
        self._TestCurrentSingleton(MySingleton, 2000)

        # Calling SetSingleton after using Push/Pop is an error: we do this so that
        # in tests we know someone is doing a SetSingleton when they shouldn't
        with pytest.raises(PushPopSingletonError):
            MySingleton.SetSingleton(MySingleton(value=10))

        # pop, returns to the initial
        MySingleton.PopSingleton()
        self._TestCurrentSingleton(MySingleton, 10)

        # SetSingleton given SingletonAlreadySet when outside Push/Pop
        with pytest.raises(SingletonAlreadySetError):
            MySingleton.SetSingleton(MySingleton(value=999))
        self._TestCurrentSingleton(MySingleton, 10)

        # The singleton set with "SetSingleton" or created automatically by "GetSingleton" is not
        # part of the stack
        with pytest.raises(PushPopSingletonError):
            MySingleton.PopSingleton()

    def testSetSingleton(self):

        class MySingleton(Singleton):

            def __init__(self, value=None):
                self.value = value

        assert not MySingleton.HasSingleton()

        MySingleton.SetSingleton(MySingleton(value=999))
        assert MySingleton.HasSingleton()
        self._TestCurrentSingleton(MySingleton, 999)

        with pytest.raises(SingletonAlreadySetError):
            MySingleton.SetSingleton(MySingleton(value=999))

        MySingleton.ClearSingleton()
        assert not MySingleton.HasSingleton()

        with pytest.raises(SingletonNotSetError):
            MySingleton.ClearSingleton()

    def testPushPop(self):

        class MySingleton(Singleton):

            def __init__(self, value=None):
                self.value = value

        MySingleton.PushSingleton()

        assert MySingleton.GetStackCount() == 1

        with pytest.raises(PushPopSingletonError):
            MySingleton.ClearSingleton()

        MySingleton.PushSingleton()
        assert MySingleton.GetStackCount() == 2

        MySingleton.PopSingleton()
        assert MySingleton.GetStackCount() == 1

        MySingleton.PopSingleton()
        assert MySingleton.GetStackCount() == 0

        with pytest.raises(PushPopSingletonError):
            MySingleton.PopSingleton()

    def testSingletonOptimization(self):

        class MySingleton(Singleton):
            pass

        def _ObtainStack(*args, **kwargs):
            self._called = True

        After(MySingleton._ObtainStack, _ObtainStack)

        self._called = False
        MySingleton.GetSingleton()
        assert self._called

        self._called = False
        MySingleton.GetSingleton()
        assert not self._called

    def testGetSingletonThreadSafe(self, mocker):
        from threading import Event, Thread

        class MySingleton(Singleton):

            @classmethod
            def SlowConstructor(cls, event):
                event.wait(1)
                return MySingleton()

        thrlist = [Thread(target=MySingleton.GetSingleton) for _ in range(3)]
        create_singleton_mock = mocker.patch.object(MySingleton, "CreateDefaultSingleton")

        event = Event()
        create_singleton_mock.side_effect = lambda: MySingleton.SlowConstructor(event)
        for thread in thrlist:
            thread.start()
        event.set()
        for thread in thrlist:
            thread.join()
        assert create_singleton_mock.call_count == 1
