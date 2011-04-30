import unittest

from myrolds import map


class ASCIICharacterMapTestCase(unittest.TestCase):

    def test_directions(self):
        asciiMap = r"""
            a-b-c
             \|/
            d-e-f
             /|\
            g-h-i
        """
        mapObj = map.ASCIICharacterMap()
        mapObj.createScapes(asciiMap)
        dirName = map.getDirectionName
        tiles = mapObj.scapes
        results = [dirName(i) for i, x in enumerate(tiles['a'].exits) if x]
        self.assertEqual(results, ['east', 'southeast'])
        results = [dirName(i) for i, x in enumerate(tiles['b'].exits) if x]
        self.assertEqual(results, ['south', 'east', 'west'])
        results = [dirName(i) for i, x in enumerate(tiles['c'].exits) if x]
        self.assertEqual(results, ['west', 'southwest'])
        results = [dirName(i) for i, x in enumerate(tiles['d'].exits) if x]
        self.assertEqual(results, ['east'])
        results = [dirName(i) for i, x in enumerate(tiles['e'].exits) if x]
        self.assertEqual(results, [
            'north', 'south', 'east', 'west', 'northeast', 'southeast',
            'southwest', 'northwest'])
        results = [dirName(i) for i, x in enumerate(tiles['f'].exits) if x]
        self.assertEqual(results, ['west'])
        results = [dirName(i) for i, x in enumerate(tiles['g'].exits) if x]
        self.assertEqual(results, ['east', 'northeast'])
        results = [dirName(i) for i, x in enumerate(tiles['h'].exits) if x]
        self.assertEqual(results, ['north', 'east', 'west'])
        results = [dirName(i) for i, x in enumerate(tiles['i'].exits) if x]
        self.assertEqual(results, ['west', 'northwest'])


class GenerateMapTestCase(unittest.TestCase):

    def test_getDirectionName(self):
        result = [map.getDirectionName(x) for x in xrange(11)]
        expected = ["north", "south", "east", "west", "northeast", "southeast",
                    "southwest", "northwest", "center", "up", "down"]
        self.assertEqual(result, expected)

    def test_generateTilesSmallMap(self):
        print
        result = map.GeneratedMap("tiny")
