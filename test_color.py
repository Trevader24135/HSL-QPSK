from color import Color
import unittest
import math
import numpy as np

class TestColorConversions(unittest.TestCase):
    def test_rgb_to_hsl(self):
        rgb = Color.from_rgb(255, 0, 0)
        hsl = rgb.as_hsl()
        self.assertEquals(hsl.shape, (1, 3))
        self.assertTrue(math.isclose(hsl[0][0], 0, rel_tol=1e-6))
        self.assertTrue(math.isclose(hsl[0][1], 1, rel_tol=1e-6))
        self.assertTrue(math.isclose(hsl[0][2], 0.5, rel_tol=1e-6))

        rgb = Color.from_rgb(0, 128, 0)
        hsl = rgb.as_hsl()
        self.assertEquals(hsl.shape, (1, 3))
        self.assertTrue(math.isclose(hsl[0][0], 120, rel_tol=1e-6))
        self.assertTrue(math.isclose(hsl[0][1], 1, rel_tol=1e-6))
        self.assertTrue(math.isclose(hsl[0][2], 0.25098039, rel_tol=1e-6))

        rgb = Color.from_rgb(64, 64, 128)
        hsl = rgb.as_hsl()
        self.assertEquals(hsl.shape, (1, 3))
        self.assertTrue(math.isclose(hsl[0][0], 240, rel_tol=1e-6))
        self.assertTrue(math.isclose(hsl[0][1], 0.33333333, rel_tol=1e-6))
        self.assertTrue(math.isclose(hsl[0][2], 0.37647059, rel_tol=1e-6))

    def test_hsl_to_rgb(self):
        hsl = Color.from_hsl(0, 1, 0.5)
        rgb = hsl.as_rgb()
        self.assertEquals(rgb.shape, (1, 3))
        self.assertTrue(math.isclose(rgb[0][0], 255, rel_tol=1))
        self.assertTrue(math.isclose(rgb[0][1], 0, rel_tol=1))
        self.assertTrue(math.isclose(rgb[0][2], 0, rel_tol=1))

        hsl = Color.from_hsl(120, 1, 0.25098039)
        rgb = hsl.as_rgb()
        self.assertEquals(rgb.shape, (1, 3))
        self.assertTrue(math.isclose(rgb[0][0], 0, rel_tol=1))
        self.assertTrue(math.isclose(rgb[0][1], 127, rel_tol=1))
        self.assertTrue(math.isclose(rgb[0][2], 0, rel_tol=1))

        hsl = Color.from_hsl(240, 0.33333333, 0.37647059)
        rgb = hsl.as_rgb()
        self.assertEquals(rgb.shape, (1, 3))
        self.assertTrue(math.isclose(rgb[0][0], 64, rel_tol=1))
        self.assertTrue(math.isclose(rgb[0][1], 64, rel_tol=1))
        self.assertTrue(math.isclose(rgb[0][2], 128, rel_tol=1))

    def test_rgb_to_hsl_array(self):
        rgb_colors = Color.from_rgb_array(np.array([
            [255, 0, 0],
            [0, 255, 0],
            [0, 0, 255],
        ]))
        hsl_colors = rgb_colors.as_hsl()
        expected_hsl = np.array([
            [0, 1, 0.5],
            [120, 1, 0.5],
            [240, 1, 0.5],
        ])
        self.assertTrue(np.all(np.equal(hsl_colors, expected_hsl)))

    def test_hsl_to_rgb_array(self):
        hsl_colors = Color.from_hsl_array(np.array([
            [0, 1, 0.5],
            [120, 1, 0.5],
            [240, 1, 0.5],
        ]))
        rgb_colors = hsl_colors.as_rgb()
        expected_rgb = np.array([
            [255, 0, 0],
            [0, 255, 0],
            [0, 0, 255],
        ])
        self.assertTrue(np.all(np.equal(rgb_colors, expected_rgb)))
