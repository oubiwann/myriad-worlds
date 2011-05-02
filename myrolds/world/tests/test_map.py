import unittest

from myrolds import util
from myrolds.const import N, S, E, W, NE, NW, SE, SW, C
from myrolds.world import map


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
        dirName = util.getDirectionName
        tiles = mapObj.scapes
        results = [dirName(i) for i, x in enumerate(tiles['a'].exits) if x]
        self.assertEqual(results, [
            'east', 'southeast'])
        results = [dirName(i) for i, x in enumerate(tiles['b'].exits) if x]
        self.assertEqual(results, [
            'south', 'east', 'west'])
        results = [dirName(i) for i, x in enumerate(tiles['c'].exits) if x]
        self.assertEqual(results, [
            'west', 'southwest'])
        results = [dirName(i) for i, x in enumerate(tiles['d'].exits) if x]
        self.assertEqual(results, [
            'east'])
        results = [dirName(i) for i, x in enumerate(tiles['e'].exits) if x]
        self.assertEqual(results, [
            'north', 'south', 'east', 'west',
            'northeast', 'southeast', 'southwest', 'northwest'])
        results = [dirName(i) for i, x in enumerate(tiles['f'].exits) if x]
        self.assertEqual(results, [
            'west'])
        results = [dirName(i) for i, x in enumerate(tiles['g'].exits) if x]
        self.assertEqual(results, [
            'east', 'northeast'])
        results = [dirName(i) for i, x in enumerate(tiles['h'].exits) if x]
        self.assertEqual(results, [
            'north', 'east', 'west'])
        results = [dirName(i) for i, x in enumerate(tiles['i'].exits) if x]
        self.assertEqual(results, [
            'west', 'northwest'])


class GenerateMapTestCase(unittest.TestCase):

    # XXX once the randomizer is in place and seeding is used, we'll be able to
    # generate predictable random maps, and thus add more tests here
    def test_generateTilesSmallMap(self):
        print
        result = map.GeneratedMap("tiny")


class MapUtilTestCase(unittest.TestCase):

    def test_getSurroundingIndicesX0Y0(self):
        grid = [
            [1, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            ]
        result = map.getSurroundingIndices(0, 0, grid)
        self.assertEqual(result[C], (0, 0))
        self.assertEqual(result[SW], None)
        self.assertEqual(result[W], None)
        self.assertEqual(result[NW], None)
        self.assertEqual(result[N], None)
        self.assertEqual(result[NE], None)
        self.assertEqual(result[E], (1, 0))
        self.assertEqual(result[SE], (1, 1))
        self.assertEqual(result[S], (0, 1))

    def test_getSurroundingIndicesX3Y0(self):
        grid = [
            [0, 0, 0, 1],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            ]
        result = map.getSurroundingIndices(3, 0, grid)
        self.assertEqual(result[C], (3, 0))
        self.assertEqual(result[SW], (2, 1))
        self.assertEqual(result[W], (2, 0))
        self.assertEqual(result[NW], None)
        self.assertEqual(result[N], None)
        self.assertEqual(result[NE], None)
        self.assertEqual(result[E], None)
        self.assertEqual(result[SE], None)
        self.assertEqual(result[S], (3, 1))

    def test_getSurroundingIndicesX3Y3(self):
        grid = [
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 1],
            ]
        result = map.getSurroundingIndices(3, 3, grid)
        self.assertEqual(result[C], (3, 3))
        self.assertEqual(result[SW], None)
        self.assertEqual(result[W], (2, 3))
        self.assertEqual(result[NW], (2, 2))
        self.assertEqual(result[N], (3, 2))
        self.assertEqual(result[NE], None)
        self.assertEqual(result[E], None)
        self.assertEqual(result[SE], None)
        self.assertEqual(result[S], None)

    def test_getSurroundingIndicesX0Y3(self):
        grid = [
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [1, 0, 0, 0],
            ]
        result = map.getSurroundingIndices(0, 3, grid)
        self.assertEqual(result[C], (0, 3))
        self.assertEqual(result[SW], None)
        self.assertEqual(result[W], None)
        self.assertEqual(result[NW], None)
        self.assertEqual(result[N], (0, 2))
        self.assertEqual(result[NE], (1, 2))
        self.assertEqual(result[E], (1, 3))
        self.assertEqual(result[SE], None)
        self.assertEqual(result[S], None)

