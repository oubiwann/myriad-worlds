import unittest

from myrolds import map


class GenerateMapTestCase(unittest.TestCase):

    def test_generateTilesSmallMap(self):
        print
        result = map.GeneratedMap("tiny").generateTiles()
