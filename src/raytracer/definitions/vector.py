"""General definitions used throughout the project."""

from __future__ import annotations
import random
import numpy as np
from typing import Any, NewType, Self, TypeVar

T = TypeVar("T", bound=np.dtype)


# TODO: fix typehint for nd array
class Vector(np.ndarray[Any, T]):
    """Implementation of a 3 dimensional vector wrapping numpy."""

    def __new__(cls, *args, **kwargs):
        this = np.array(*args, **kwargs)
        this = np.asarray(this).view(cls)
        return this

    def __array_finalize__(self, obj):
        # Ensure that the vector has 3 components only when the shape is not empty
        if obj is None:
            return
        if self.shape != ():  # Ensure it's not an intermediate step
            self.ensure_vector3()

    def ensure_vector3(self):
        if self.shape != (3,):
            raise ValueError(
                f"Array must be a vector with 3 entries but {self=}, {self.shape=}."
            )

    @property
    def x(self) -> T:
        return self[0]

    @property
    def y(self) -> T:
        return self[1]

    @property
    def z(self) -> T:
        return self[2]

    def length(self) -> float:
        return np.linalg.norm(self)

    @classmethod
    def random(cls, lower=0.0, upper=1.0) -> Self:
        return cls(
            [
                random.uniform(lower, upper),
                random.uniform(lower, upper),
                random.uniform(lower, upper),
            ]
        )

    @classmethod
    def random_unit_vector(cls) -> Self:
        while True:
            p = cls.random(-1, 1)
            length = p.length()
            if 10**-100 < length <= 1:
                return p / length

    @classmethod
    def random_on_hemisphere(cls, normal: Vector) -> Self:
        unit_vector = cls.random_unit_vector()
        if np.dot(unit_vector, normal) < 0.0:
            return -unit_vector
        else:
            return unit_vector


def unit_vector(v: Vector) -> Vector:
    """Returns a unit vector with the same direction."""
    return v / np.linalg.norm(v)


Point = NewType("Point", Vector)
Color = NewType("Color", Vector)
