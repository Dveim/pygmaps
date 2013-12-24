# -*- coding: utf-8 -*-

import unittest
import pygmaps


class TestPygmaps(unittest.TestCase):
    def test_get_distance_small_distance(self):
        res = pygmaps.get_distance(origin='Київ, Хрещатик 1', destination='Київ, Хрещатик 3')
        self.assertAlmostEqual(res, 550, msg="Wrong distance", delta=30)

    def test_get_distance_big_distance(self):
        res = pygmaps.get_distance(origin='Kiev', destination='Lviv')
        self.assertAlmostEqual(res, 540000, msg="Wrong distance", delta=1000)

    def test_get_distance_latlng(self):
        x1 = 50.4501
        y1 = 30.5234
        x2 = 49.8396
        y2 = 24.0297
        res1 = pygmaps.get_distance(origin=(x1, y1), destination=(x2, y2))
        res2 = pygmaps.get_distance(origin='Kiev', destination='Lviv')
        self.assertAlmostEqual(res1, res2, msg="Wrong time from Kiev to Lviv", delta=200)


if __name__ == '__main__':
    unittest.main()