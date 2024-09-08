from raytracer.color import hit_sphere, write_color
import io

from raytracer.definitions import Color, Point, Vector
from raytracer.ray import Ray


def test_color():
    out = io.StringIO()
    write_color(out, Color(Vector([0, 0.1, 1.0])))
    assert out.getvalue() == "0 25 255\n"


def test_hit_sphere_two():
    # GIVEN a point at [0, 0, -1] with radius 0.5
    center = Point(Vector([0, 0, -1]))
    radius = 0.5

    # WHEN a ray from the origin points towards [0, 0, -1]
    ray = Ray(Point(Vector([0, 0, 0])), direction=Vector([0, 0, -1]))

    # THEN the ray hits the ponit
    assert hit_sphere(center, radius, ray)


def test_hit_sphere_one():
    # GIVEN a point at [0, 0, -1] with radius 0.5
    center = Point(Vector([0, 0, -1]))
    radius = 0.5

    # WHEN a ray is pointed towards [0.5, 0, -1]
    ray = Ray(Point(Vector([0, 0, 0])), direction=Vector([0.5, 0, -1]))

    # THEN the ray is hit in one location
    assert hit_sphere(center, radius, ray)


def test_hit_sphere_zero():
    # GIVEN a point at [0, 0, -1] with radius 0.5
    center = Point(Vector([0, 0, -1]))
    radius = 0.5

    # WHEN a ray is pointed towards [0.5, 0.5, -1]
    ray = Ray(Point(Vector([0, 0, 0])), direction=Vector([0.5, 0.5, -1]))

    # THEN the ray is never hit
    assert not hit_sphere(center, radius, ray)
