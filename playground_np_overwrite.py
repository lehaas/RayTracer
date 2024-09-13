import numpy as np


class NDArray3D(np.ndarray):
    def __new__(cls, *args, **kwargs):
        this = np.array(*args, **kwargs)
        this = np.asarray(this).view(cls)
        return this

    def __array_finalize__(self, obj):
        self.ensure_3d_shape()

    def ensure_3d_shape(self):
        if self.ndim != 3:
            raise ValueError("Array must be 3-dimensional.")


arr1 = NDArray3D(np.random.rand(2, 3, 4))
arr2 = NDArray3D(np.random.rand(2, 3, 4))

# Add two NDArray3D instances
result = arr1 + arr2
print(result)

# Multiply NDArray3D by a scalar
result = arr1 * 2
print(result)

# This will raise an error
arr3 = NDArray3D(np.random.rand(2, 3))
