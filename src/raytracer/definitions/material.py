import abc

import numpy as np
from raytracer.definitions.ray import Ray
from raytracer.definitions.vector import Color, Point, Vector, unit_vector


class Material(abc.ABC):
    @abc.abstractmethod
    def scatter(
        self, ray: Ray, normal: Vector, intersection: Point, front_facing: bool
    ) -> Vector | None:
        """Scatter ray on the object with given normal and intersection point.

        Args:
            ray: incomming ray.
            normal: normal of the scattering object.
            intersection: intersection between the ray and the object.
            front_facing: True if the ray is facing the front of the object, i.e., inwards facing.
        """

    @property
    @abc.abstractmethod
    def attentuition(self) -> Color:
        pass


class DefaultMaterial(Material):
    def scatter(
        self, ray: Ray, normal: Vector, intersection: Point, front_facing: bool
    ) -> Vector | None:
        return None

    @property
    def attentuition(self) -> Color:
        return Color(Vector([0.0, 0.0, 0.0]))


class Lambertian(Material):
    def __init__(self, albedo: Color):
        self.albedo = albedo

    def scatter(
        self, ray: Ray, normal: Vector, intersection: Point, front_facing: bool
    ) -> Vector | None:
        scatter_direction = normal + Vector.random_unit_vector()
        scattered = Ray(intersection, scatter_direction)
        return scattered

    @property
    def attentuition(self) -> Color:
        return self.albedo


class Metal(Material):
    def __init__(self, albedo: Color, fuzz: float):
        self.albedo = albedo
        self.fuzz = fuzz

        assert 0 <= self.fuzz <= 1

    def scatter(
        self, ray: Ray, normal: Vector, intersection: Point, front_facing: bool
    ) -> Vector | None:
        reflected = reflect(ray.direction, normal)
        reflected = unit_vector(reflected) + self.fuzz * Vector.random_unit_vector()
        scattered = Ray(intersection, reflected)

        if np.dot(scattered.direction, normal) > 0:
            return scattered
        else:
            return None

    @property
    def attentuition(self) -> Color:
        return self.albedo


def reflect(v1: Vector, v2: Vector) -> Vector:
    return v1 - 2 * np.dot(v1, v2) * v2


class Dialetric(Material):
    def __init__(self, attentuition: float, refraction_index: float):
        self._attentuition = attentuition
        self.refraction_index = refraction_index

    def scatter(
        self, ray: Ray, normal: Vector, intersection: Point, front_facing: bool
    ) -> Vector | None:
        refraction_index = (
            1 / self.refraction_index if front_facing else self.refraction_index
        )
        refracted = refract(unit_vector(ray.direction), normal, refraction_index)
        return Ray(intersection, refracted)

    @property
    def attentuition(self) -> Color:
        return self._attentuition


def refract(v: Vector, n: Vector, relative_refraction: float) -> Vector:
    """Refract v at an object with normal n and given relative refraction.

    Args:
        v: incomming vector
        n: normal of the refracting surface
        relative_refraction: relativet refraction of the objects (eta_in / eta_out)
    """
    assert abs(v.length() - 1) < 10e-10, f"{v=} is supposed to be a unit vector."
    assert abs(n.length() - 1) < 10e-10, f"{n=} is supposed to be a unit vector."

    cos_theta = min(np.dot(-v, n), 1.0)
    r_perp = relative_refraction * (v + cos_theta * n)
    r_para = -np.sqrt(1 - r_perp.length() ** 2) * n

    return r_perp + r_para
