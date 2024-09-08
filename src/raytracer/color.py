import io
from typing import Optional

import numpy as np


from raytracer.definitions import Color, Point, Vector, unit_vector
from raytracer.ray import Ray


def write_color(out: io.StringIO, pixel_color: Color) -> None:
    """Write a color to the output.

    Args:
        out: output stream
        color: 3D vector of floats in [0,1].
    """
    assert 0.0 <= pixel_color[0] <= 1.0
    assert 0.0 <= pixel_color[1] <= 1.0
    assert 0.0 <= pixel_color[2] <= 1.0

    r, g, b = pixel_color

    out.write(f"{int(255.999 * r)} {int(255.999 * g)} {int(255.999 * b)}\n")


WHITE = Color(Vector([1.0, 1.0, 1.0]))
BLUE = Color(Vector([0.5, 0.7, 1.0]))


def hit_sphere_at(center: Point, radius: float, ray: Ray) -> Optional[float]:
    """Returns the distance to the sphere or None if there is no intersection.

    TODO: currently spheres in front and behind the camera are hit.
    """
    oc = center - ray.orig
    a = np.dot(ray.dir, ray.dir)
    b = -2 * np.dot(ray.dir, oc)
    c = np.dot(oc, oc) - radius**2
    discriminant = b**2 - 4 * a * c

    if discriminant >= 0:
        return (-b - np.sqrt(discriminant)) / (2 * a)
    else:
        return None


def color_ray(ray: Ray) -> Color:
    center = Point(Vector([0, 0, -1]))
    if d := hit_sphere_at(center, 0.5, ray):
        # compute the distance from center to hit point
        v = unit_vector(ray.at(d) - center)
        # v is in [-1, 1]: scale it to [0, 1]
        return Color(0.5 * (v + 1))
    v = unit_vector(ray.dir)
    a = 0.5 * (v.y + 1.0)
    return (1.0 - a) * WHITE + a * BLUE
