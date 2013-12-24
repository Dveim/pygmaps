# -*- coding: utf-8 -*-

import unittest
import pygmaps


class TestPygmaps(unittest.TestCase):
    def test_get_time_small_distance(self):
        res = pygmaps.get_time(origin='Київ, Хрещатик 1', destination='Київ, Хрещатик 3', mode='walking')
        self.assertLess(res, 1000, "Too big time for walking")

    def test_get_time_big_distance(self):
        res = pygmaps.get_time(origin='Kiev', destination='Lviv', mode='transit')
        self.assertLess(res, 30000, "Wrong time from Kiev to Lviv")

    def test_get_time_latlng(self):
        x1 = 50.4501
        y1 = 30.5234
        x2 = 49.8396
        y2 = 24.0297
        res1 = pygmaps.get_time(origin=(x1, y1), destination=(x2, y2))
        res2 = pygmaps.get_time(origin='Kiev', destination='Lviv')
        self.assertAlmostEqual(res1, res2, msg="Wrong time from Kiev to Lviv", delta=50)


if __name__ == '__main__':
    unittest.main()