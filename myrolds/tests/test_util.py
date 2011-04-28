import unittest

from myrolds import util
from myrolds.const import N, S, E, W, NE, NW, SE, SW, C


class UtilTestCase(unittest.TestCase):

    def test_getRandomIntsGetOne(self):
        result = util.getRandomInts(0, 1, 1, 1)
        self.assertEqual(len(result), 1)

    def test_getRandomIntsGet2Step5(self):
        result = util.getRandomInts(min=5, max=15, step=5, count=2)
        self.assertEqual(len(result), 2)
        self.assertIn(True, [x in result for x in [5, 10, 15]])
        self.assertNotIn(0, result)
        self.assertNotIn(1, result)

    def test_getRandomIntsGet100(self):
        result = util.getRandomInts(0, 2, 1, 100)
        self.assertEqual(len(result), 100)
        self.assertIn(0, result)
        self.assertIn(1, result)
        self.assertIn(2, result)
        self.assertNotIn(3, result)
   
    def test_getRandomIntsGet100Step10(self):
        result = util.getRandomInts(0, 30, 10, 100)
        self.assertEqual(len(result), 100)
        self.assertIn(0, result)
        self.assertIn(10, result)
        self.assertIn(20, result)
        self.assertIn(30, result)
        self.assertNotIn(40, result)
   
    def test_getTileClasses(self):
        result = util.getTileClasses()
        self.assertEqual(len(result), 15)

    def test_getSurroundingIndicesX0Y0(self):
        grid = [
            [1, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            ]
        result = util.getSurroundingIndices(0, 0, grid)
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
        result = util.getSurroundingIndices(3, 0, grid)
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
        result = util.getSurroundingIndices(3, 3, grid)
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
        result = util.getSurroundingIndices(0, 3, grid)
        self.assertEqual(result[C], (0, 3))
        self.assertEqual(result[SW], None)
        self.assertEqual(result[W], None)
        self.assertEqual(result[NW], None)
        self.assertEqual(result[N], (0, 2))
        self.assertEqual(result[NE], (1, 2))
        self.assertEqual(result[E], (1, 3))
        self.assertEqual(result[SE], None)
        self.assertEqual(result[S], None)
