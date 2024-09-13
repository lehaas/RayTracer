import abc
from typing import Optional

import numpy as np

from raytracer.definitions.material import DefaultMaterial, Material
from raytracer.definitions.vector import Point
from raytracer.definitions.ray import Ray
from raytracer.definitions.hit_record import Record


class Hittable(abc.ABC):
    @abc.abstractmethod
    def hit(self, ray: Ray, t_min: float, t_max: float) -> Optional[Record]:
        """Compute the intersection of the ray and the hittable, else return None."""


def is_front_facing(ray: Ray, outward_normal):
    return np.dot(ray.direction, outward_normal) < 0


class Sphere(Hittable):
    def __init__(self, center: Point, radius: float, material: Material | None = None):
        self.center = center
        self.radius = radius
        self.material = material or DefaultMaterial()

    def hit(self, ray: Ray, t_min: float = 0.0, t_max: float = 1.0) -> Optional[Record]:
        """Returns the distance to the sphere or None if there is no intersection.

        TODO: currently spheres in front and behind the camera are hit.
        """
        a, h, discriminant = self._compute_discriminant(ray)

        if discriminant < 0:
            return None

        t = self._compute_closest_root(a, h, discriminant, t_min, t_max)

        if not t:
            return None

        return self._compute_record(ray, t)

    def _compute_record(self, ray, t):
        p = ray.at(t)
        outward_normal = (p - self.center) / self.radius
        front_facing = is_front_facing(ray, outward_normal)
        return Record(
            point=p,
            normal=(1 if front_facing else -1) * outward_normal,
            front_facing=front_facing,
            distance=t,
            material=self.material,
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
