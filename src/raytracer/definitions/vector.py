"""General definitions used throughout the project."""

import numpy as np
from typing import Any, NewType, TypeVar

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


def unit_vector(v: Vector) -> Vector:
    """Returns a unit vector with the same direction."""
    return v / np.linalg.norm(v)


Point = NewType("Point", Vector)
Color = NewType("Color", Vector)
