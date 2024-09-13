from dataclasses import dataclass
import numpy as np
from raytracer.definitions.material import Material
from raytracer.definitions.vector import Point, Vector


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
    front_facing: bool
    material: Material

    def __eq__(self, other):
        if not isinstance(other, Record):
            return False
        return (
            np.array_equal(self.point, other.point)
            and np.array_equal(self.normal, other.normal)
            and self.distance == other.distance
        )
