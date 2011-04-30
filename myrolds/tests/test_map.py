import unittest

from myrolds import map


class GenerateMapTestCase(unittest.TestCase):

    def test_getDirectionName(self):
        result = [map.getDirectionName(x) for x in xrange(11)]
        expected = ["north", "south", "east", "west", "northeast", "southeast",
                    "southwest", "northwest", "center", "up", "down"]
        self.assertEqual(result, expected)

    def test_generateTilesSmallMap(self):
        print
        result = map.GeneratedMap("tiny")
