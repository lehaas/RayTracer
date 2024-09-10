from typing import Optional, Self
from raytracer.definitions.ray import Ray
from raytracer.hitable import Hittable, Record


class World:
    def __init__(self):
        self.hittables: list[Hittable] = []

    def add(self, h: Hittable) -> Self:
        self.hittables.append(h)
        return self

    def hit(self, ray: Ray, t_min: float, t_max: float) -> Optional[Record]:
        closest_dist = t_max
        record = None

        for hittable in self.hittables:
            if r := hittable.hit(ray, t_min, closest_dist):
                record = r
                closest_dist = r.distance

        return record
