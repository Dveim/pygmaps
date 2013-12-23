# -*- coding: utf-8 -*-

import unittest
import pygmaps


class TestPygmaps(unittest.TestCase):
    def test_get_distance_small_distance(self):
        res = pygmaps.get_distance(origin='Київ, Хрещатик 1', destination='Київ, Хрещатик 3')
        self.assertEqual(res, 537, "Wrong distance")

    def test_get_distance_big_distance(self):
        res = pygmaps.get_distance(origin='Kiev', destination='Lviv')
        self.assertGreater(res, 20000, "Wrong distance")

    def test_get_time_small_distance(self):
        res = pygmaps.get_time(origin='Київ, Хрещатик 1', destination='Київ, Хрещатик 3', mode='walking')
        self.assertLess(res, 1000, "Too big time for walking")

    def test_get_time_big_distance(self):
        res = pygmaps.get_time(origin='Kiev', destination='Lviv', mode='transit')
        self.assertGreater(res, 20000, "Wrong time from Kiev to Lviv")


if __name__ == '__main__':
    unittest.main()