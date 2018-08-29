from __future__ import unicode_literals

'''
Functions and utilities for naming objects, as they will be displayed to the user.
'''


#===================================================================================================
# GetUnusedName
#===================================================================================================
def GetUnusedName(names, prefix):
    '''
    Return a new name that is not in the given sequence of names. Useful to name new entities in
    the application. For instance, a prefix "Alpha" will return names like "Alpha 1" and "Alpha 2".

    :type names: C{list}
    :param names:
        list with names already present

    :type prefix: C{unicode}
    :param prefix:
        name prefix

    :rtype: C{unicode}
    :returns:
        the new name
    '''
    # defining new name (smart)
    names = set(names)
    count = 1
    while True:
        new_name = '%s %d' % (prefix, count)
        if new_name not in names:
            return new_name
        count += 1
