from raytracer.definitions import Vector
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
