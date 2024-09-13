import abc

import numpy as np
from raytracer.definitions.ray import Ray
from raytracer.definitions.vector import Color, Point, Vector, unit_vector


class Material(abc.ABC):
    @abc.abstractmethod
    def scatter(self, ray: Ray, normal: Vector, point: Point) -> Vector | None:
        pass


class DefaultMaterial(Material):
    def scatter(self, ray: Ray, normal: Vector, point: Point) -> Vector | None:
        return None


class Lambertian(Material):
    def __init__(self, albedo: Color):
        self.albedo = albedo

    def scatter(self, ray: Ray, normal: Vector, point: Point) -> Vector | None:
        scatter_direction = normal + Vector.random_unit_vector()
        scattered = Ray(point, scatter_direction)
        return scattered


class Metal(Material):
    def __init__(self, albedo: Color, fuzz: float):
        self.albedo = albedo
        self.fuzz = fuzz

        assert 0 <= self.fuzz <= 1

    def scatter(self, ray: Ray, normal: Vector, point: Point) -> Vector | None:
        reflected = reflect(ray.direction, normal)
        reflected = unit_vector(reflected) + self.fuzz * Vector.random_unit_vector()
        scattered = Ray(point, reflected)

        if np.dot(scattered.direction, normal) > 0:
            return scattered
        else:
            return None


def reflect(v1: Vector, v2: Vector) -> Vector:
    return v1 - 2 * np.dot(v1, v2) * v2
