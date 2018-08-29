from __future__ import absolute_import, unicode_literals

from coilib50 import unittest
from coilib50.basic.naming import GetUnusedName


#===================================================================================================
# Test
#===================================================================================================
class Test(unittest.TestCase):

    def testGetUnusedName(self):
        self.assertEqual(GetUnusedName([], 'Alpha'), 'Alpha 1')

        names = ['Alpha 1', 'Alpha 2', 'Alpha 3']
        self.assertEqual(GetUnusedName(names, 'Alpha'), 'Alpha 4')

        names = ['Alpha 1', 'Alpha 3']
        self.assertEqual(GetUnusedName(names, 'Alpha'), 'Alpha 2')


#===================================================================================================
# Entry Point
#===================================================================================================
if __name__ == '__main__':
    unittest.main()
