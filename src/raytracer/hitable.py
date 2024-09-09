import abc
from dataclasses import dataclass
from typing import Optional

import numpy as np

from raytracer.definitions import Point, Vector
from raytracer.ray import Ray


@dataclass
class Record:
    """Record a hit between a hittable and a ray

    Attributes:
        point: insection point between hittable and ray
        normal: normal of the hittable and the ray at the intersection point
        distance: distance from the ray origin to the intersection point
    """

    point: Point
    normal: Vector
    distance: float

    def __eq__(self, other):
        if not isinstance(other, Record):
            return False
        return (
            np.array_equal(self.point, other.point)
            and np.array_equal(self.normal, other.normal)
            and self.distance == other.distance
        )


class Hittable(abc.ABC):
    @abc.abstractmethod
    def hit(self, ray: Ray, ray_tmin: float, ray_tmax: float) -> Optional[Record]:
        """Compute the intersection of the ray and the hittable, else return None."""


def is_front_facing(ray: Ray, outward_normal):
    return np.dot(ray.direction, outward_normal) < 0


class Sphere(Hittable):
    def __init__(self, center: Point, radius: float):
        self.center = center
        self.radius = radius

    def hit(self, ray: Ray, t_min: float = 0.0, t_max: float = 1.0) -> Optional[Record]:
        """Returns the distance to the sphere or None if there is no intersection.

        TODO: currently spheres in front and behind the camera are hit.
        """
        a, h, discriminant = self._compute_discriminant(ray)

        if discriminant < 0:
            return False

        t = self._compute_closest_root(a, h, discriminant, t_min, t_max)

        if not t:
            return False

        p = ray.at(t)
        outward_normal = (p - self.center) / self.radius
        return Record(
            point=p,
            normal=(
                outward_normal
                if is_front_facing(ray, outward_normal)
                else -outward_normal
            ),
            distance=t,
        )

    def _compute_closest_root(
        self, a: float, h: float, discriminant: float, t_min: float, t_max: float
    ) -> Optional[float]:
        root = (h - np.sqrt(discriminant)) / a
        if not t_min <= root <= t_max:
            root = (h - np.sqrt(discriminant)) / a
            if not t_min <= root <= t_max:
                return None

        return root

    def _compute_discriminant(self, ray):
        oc = self.center - ray.orig
        a = np.linalg.norm(ray.direction) ** 2
        h = np.dot(ray.direction, oc)
        c = np.linalg.norm(oc) ** 2 - self.radius**2
        discriminant = h * h - a * c
        return a, h, discriminant
