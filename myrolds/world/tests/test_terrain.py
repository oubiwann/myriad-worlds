import unittest

from myrolds.world import terrain


class TerrainUtilTestCase(unittest.TestCase):

    def test_getTileClasses(self):
        result = terrain.getTileClasses()
        self.assertEqual(len(result), 15)