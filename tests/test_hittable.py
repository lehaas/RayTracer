import numpy as np

from raytracer.definitions import Point, Vector
from raytracer.hitable import Record, Sphere
from raytracer.ray import Ray


def test_hit_sphere_two():
    """Test if hit_sphere returns the cloesest distance if multiple hits exist."""
    # GIVEN a point at [0, 0, -1] with radius 0.5
    sphere = Sphere(Point(Vector([0, 0, -1])), radius=0.5)

    # WHEN a ray from the origin points towards [0, 0, -1]
    ray = Ray(Point(Vector([0, 0, 0])), direction=Vector([0, 0, -1]))

    # THEN the ray hits the sphere
    assert sphere.hit(ray) == Record(
        Point(Vector([0, 0, -0.5])), Vector([0.0, 0.0, 1.0]), 0.5
    )


def test_hit_sphere_one():
    """Test if hit_sphere returns the correct distance for a single hit.

    Solving the equation here:
    https://raytracing.github.io/books/RayTracingInOneWeekend.html#addingasphere/ray-sphereintersection
    for a single intersection returns that at [sqrt(1/3), 0, -1], there is only a single intersection.
    """
    # GIVEN a point at [0, 0, -1] with radius 0.5
    sphere = Sphere(center=Point(Vector([0, 0, -1])), radius=0.5)

    # WHEN a ray is pointed towards [sqrt(1/3), 0, -1]
    ray = Ray(Point(Vector([0, 0, 0])), direction=Vector([np.sqrt(1 / 3), 0, -1]))

    # THEN the ray hits the sphere in one location
    assert sphere.hit(ray) == Record(
        Point(Vector([np.sqrt(1 / 3), 0, -1])),
        # TODO: I am a bit sceptic that this vector is aligned with the x-axis. Double-check!
        Vector([-2 * np.sqrt(1 / 3), 0.0, 0.0]),
        1,
    )


def test_hit_sphere_zero():
    """Test that hit_sphere returns None if no hit exists."""
    # GIVEN a point at [0, 0, -1] with radius 0.5
    sphere = Sphere(center=Point(Vector([0, 0, -1])), radius=0.5)

    # WHEN a ray is pointed towards [0.5, 0.5, -1]
    ray = Ray(Point(Vector([0, 0, 0])), direction=Vector([0.5, 0.5, -1]))

    # THEN the ray is never hit
    assert not sphere.hit(ray)
