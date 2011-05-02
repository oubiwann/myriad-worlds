import unittest

from myrolds import util


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

    def test_getDirectionName(self):
        result = [util.getDirectionName(x) for x in xrange(11)]
        expected = ["north", "south", "east", "west", "northeast", "southeast",
                    "southwest", "northwest", "center", "up", "down"]
        self.assertEqual(result, expected)
