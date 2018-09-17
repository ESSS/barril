from __future__ import unicode_literals

import threading


#===================================================================================================
# SingletonError
#===================================================================================================
class SingletonError(RuntimeError):
    '''
    Base class for all Singleton-related exceptions.
    '''


#===================================================================================================
# SingletonAlreadySetError
#===================================================================================================
class SingletonAlreadySetError(SingletonError):
    '''
    Trying to set a singleton when the class already have one defined.
    '''


#===================================================================================================
# SingletonNotSetError
#===================================================================================================
class SingletonNotSetError(SingletonError):
    '''
    Trying to clear a singleton when there's none defined.
    '''


#===================================================================================================
# PushPopSingletonError
#===================================================================================================
class PushPopSingletonError(SingletonError):
    '''
    Trying to set a singleton between a PushSingleton/PopSingleton calls.
    '''


#===================================================================================================
# Singleton
#===================================================================================================
class Singleton(object):
    '''
    Base class for singletons.

    A Singleton class should have a unique instance during the lifetime of the application. Besides
    the functionality of obtaining the singleton instance, this class also provides methods to push
    and pop singletons, useful for testing, where you push a singleton into a known state during
    setUp and pops it back during tearDown
    '''

    # name of the attribute that holds the stack of singletons
    __singleton_stack_start_index = 0
    __lock = threading.RLock()

    _singleton_classes = set()

    @staticmethod
    def ResetDefaultSingletonInstances():
        '''
        This singleton class is intended to be used in tests with the push / pop protocol. However some singleton
        dependencies might be hidden away from the test creator (or even be introduced after the test creation) making
        easy for a code to access and change the default class singleton (for example registering on its callbacks).

        This code is intended to clear any change made in such default singletons. Pushed singletons will not be cleared
        because if a test has correctly pushed it singleton, it is reasonable to assume that the test will correctly
        clean (pop) it.

        TODO: ETK-1235 As soon as the classes with ResetInstance are moved to do not be a singleton, then this method
        can be removed.
        '''
        for cls in Singleton._singleton_classes:
            if cls._UsingDefaultSingleton():
                instance = cls.GetSingleton()
                instance.ResetInstance()

    @classmethod
    def GetSingleton(cls):
        '''
        :rtype: Singleton
        :returns:
            Returns the current singleton instance.

        .. note:: This function is thread-safe, but all the other methods (such as SetSingleton,
            PushSingleton, PopSingleton, etc) are not (which should be Ok as those are mostly
            test-related, as singletons shouldn't really be changed after the application is up
            especially on multi-threaded environments).
        '''
        Singleton._singleton_classes.add(cls)

        try:
            # Make common case faster.
            return cls.__singleton_singleton_stack__[-1]
        except (AttributeError, IndexError):
            with cls.__lock:
                # Only lock if the 'fast path' did not work.
                stack = cls._ObtainStack()

                if not stack:  # Faster than doing len(stack) == 0
                    return cls.SetSingleton(None)

                return stack[-1]

    @classmethod
    def SetSingleton(cls, instance):
        '''
        Sets the current singleton.

        :param Singleton instance:
            The Singleton to pass as parameter

        :rtype: Singleton
        :returns:
            The singleton passed as parameter.

        @raise PushPopSingletonError
        @raise SingletonAlreadySetError
        '''
        stack = cls._ObtainStack()

        # Error if we trying to use SetSingleton between a Push/Pop
        if len(stack) != cls.__singleton_stack_start_index:
            raise PushPopSingletonError('SetSingleton can not be called between a Push/Pop pair.')

        if len(stack) > 0:
            raise SingletonAlreadySetError('SetSingleton can only be called when there is no singleton set.')

        # Obtain default instance (if needed)
        if instance is None:
            instance = cls.CreateDefaultSingleton()

        # Set the stack[0] as the singleton
        if len(stack) == 0:
            stack.append(instance)
            cls.__singleton_stack_start_index = 1
        else:
            stack[0] = instance

        assert cls.__singleton_stack_start_index == 1

        return instance

    @classmethod
    def _UsingDefaultSingleton(cls):
        '''
        Checks if the current singleton instance is the default instance.

        :rtype: bool
        :returns:
            True if the current singleton instance is the default created instance. Returns False if the current instance
            is a pushed singleton or if no instance is currently set
        '''
        stack = cls._ObtainStack()
        has_pushed = len(stack) != cls.__singleton_stack_start_index
        has_singleton = cls.HasSingleton()

        return has_singleton and not has_pushed

    def ResetInstance(self):
        '''
        Restore the instance original configuration. Singleton classes should not have a internal state to reset
        (as described in issue ETK-1235), so subclasses that implement this method are strong candidates to be refactored
        to do not be a singleton.

        This method is used to avoid interference between tests while ETK-1235 is not implemented.
        '''
        pass

    @classmethod
    def ClearSingleton(cls):
        '''
        Clears the current singleton
        '''
        stack = cls._ObtainStack()

        # Error if we trying to use ClearSingleton between a Push/Pop
        if len(stack) != cls.__singleton_stack_start_index:
            raise PushPopSingletonError('ClearSingleton can not be called between a Push/Pop pair.')

        if not stack:
            raise SingletonNotSetError('ClearSingleton can only be called when THERE IS singleton set.')

        del stack[0]
        cls.__singleton_stack_start_index = 0

    @classmethod
    def HasSingleton(cls):
        '''
        Do we have any singleton set?

        :rtype: bool
        :returns:
            True if there's a singleton set.
        '''
        stack = cls._ObtainStack()
        return len(stack) > 0

    @classmethod
    def CreateDefaultSingleton(cls):
        '''
        Creates the default singleton instance, that will be used when no singleton has been installed.
        By default, tries to create the class without constructor.

        :rtype: Singleton
        :returns:
            an instance of the singleton subclass
        '''
        return cls()

    # Push/Pop -------------------------------------------------------------------------------------

    @classmethod
    def PushSingleton(cls, instance=None):
        '''
        Pushes the given singleton to the top of the stack. The previous singleton will be restored
        when PopSingleton is called.

        :param Singleton instance:
            The singleton to install as the current one. If not given, a new singleton default
            is created.

        :rtype: Singleton
        :returns:
            The current singleton.
        '''
        if instance is None:
            instance = cls.CreateDefaultSingleton()
        stack = cls._ObtainStack()

        stack.append(instance)
        return instance

    @classmethod
    def PopSingleton(cls):
        '''
        Restores the singleton that was the current before the last PushSingleton.

        :rtype: Singleton
        :returns:
            Return the removed singleton.
        '''
        stack = cls._ObtainStack()

        if len(stack) == cls.__singleton_stack_start_index:
            raise PushPopSingletonError('PopSingleton called without a pair PushSingleton call')

        return cls._ObtainStack().pop(-1)

    @classmethod
    def _ObtainStack(cls):
        '''
        Obtains the stack of singletons.

        :rtype: list
        :returns:
            The singleton stack.
        '''
        try:
            return cls.__singleton_singleton_stack__
        except AttributeError:
            assert cls is not Singleton, 'This method can only be called from a Singleton subclass.'
            stack = []
            cls.__singleton_singleton_stack__ = stack
            return stack

    @classmethod
    def GetStackCount(cls):
        '''
        @return int:
            The number of elements added int the stack using PushSingleton.
        '''
        stack = cls._ObtainStack()
        return len(stack) - cls.__singleton_stack_start_index
