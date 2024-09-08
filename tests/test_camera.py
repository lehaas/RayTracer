import numpy as np
from raytracer.definitions import Point, Vector
from raytracer.main import Camera


def test_simple():
    viewport_height = 10
    viewport_width = 12
    camera = Camera(1, viewport_height, viewport_width, Point(Vector([0.0, 0.0, 0.0])))

    np.testing.assert_equal(camera.viewport_u, Vector([viewport_width, 0, 0]))
    np.testing.assert_equal(camera.viewport_v, Vector([0, -viewport_height, 0]))
    np.testing.assert_equal(camera.viewport_upper_left, Vector([-6, 5, -1]))
