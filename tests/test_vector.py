import numpy as np
from raytracer.definitions import Vector, unit_vector
import pytest


def test_vector():
    """Test that 3 entries vectors can be created and results are again vectors"""
    # GIVEN 2 Vectors
    a = Vector([1, 2, 3])
    b = Vector([1, 2, 3])

    # WHEN applying a numpy operation
    # THEN the result is a again a Vector
    assert isinstance(a + b, Vector)
    assert isinstance(a * b, Vector)


def test_wrong_shape():
    # GIVEN a broken Vector definition
    # WHEN creating the Vector
    # THEN a ValueError is raised
    with pytest.raises(ValueError):
        Vector([1, 2])

    with pytest.raises(ValueError):
        Vector([[1, 2, 3], [1, 2, 3]])


def test_xyz():
    """Test that x, y, and z return the correct values."""
    v = Vector([1, 2, 3])
    assert v.x == 1
    assert v.y == 2
    assert v.z == 3


@pytest.mark.parametrize(
    ["_in", "out"],
    [
        (Vector([3, 0, 0]), Vector([1, 0, 0])),
        (Vector([2, 2, 2]), Vector([1 / np.sqrt(3), 1 / np.sqrt(3), 1 / np.sqrt(3)])),
        (Vector([3, 0, 0]), Vector([1, 0, 0])),
    ],
)
def test_unit_vector(_in: Vector, out: Vector):
    """Test that unit_vector returns a unit vector."""

    np.testing.assert_equal(unit_vector(_in), out)
