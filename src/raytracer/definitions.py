"""General definitions used throughout the project.

TODO:
- refactor Vector
    - is there a way to just type a 3-dimensional numpy array?
    - how to define a low-level wrapper of numpy arrays, that still allows all operations?
"""

import numpy as np
from typing import NewType, TypeVar

T = TypeVar("T", bound=np.generic)


class Vector(np.ndarray):
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
                f"Array must be a vector with 3 entries but {self.shape=}."
            )


Point = NewType("Point", Vector)
Color = NewType("Color", Vector)
