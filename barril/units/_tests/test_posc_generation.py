from __future__ import absolute_import, unicode_literals

from coilib50 import unittest
from coilib50.units import resource_additional_units, resource_posc_units_22
from coilib50.units.unit_database import UnitDatabase


#===================================================================================================
# Test
#===================================================================================================
class Test(unittest.TestCase):

    def testGenerate(self):

        class Cog(object):

            def __init__(self):
                self.contents = []

            def outl(self, contents=''):
                self.contents.append(contents)

        from coilib50.units import _posc_generation
        cog = Cog()
        _posc_generation.GenerateDatabaseCodeCOG(cog, [
            resource_posc_units_22.GetData().decode('utf-8'),
            resource_additional_units.GetData().decode('utf-8'),
        ])
        contents = '\n'.join(cog.contents)

        # Uncomment for tests
        # open('posc_generated_database.py', 'w').write(contents)
        obj = compile(contents, '<string>', 'exec')

        db = UnitDatabase()
        locs = dict(
            db=db,
            fill_categories=True,
            override_categories=False,
            MakeCustomaryToBase=_posc_generation.MakeCustomaryToBase,
            MakeBaseToCustomary=_posc_generation.MakeBaseToCustomary,
        )

        exec(obj, globals(), locs)


#===================================================================================================
# main
#===================================================================================================
if __name__ == '__main__':
    unittest.main()
