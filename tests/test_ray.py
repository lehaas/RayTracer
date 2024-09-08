import pytest
from raytracer.definitions import Point, Vector
from raytracer.ray import Ray

_ZERO = Vector([0.0, 0.0, 0.0])


@pytest.mark.parametrize(
    ["origin", "direction", "magnitude", "result"],
    [
        (Point(_ZERO), _ZERO, 0, Point(_ZERO)),
        (Point(_ZERO), _ZERO, 10, Point(_ZERO)),
        (Point([1, 2, 3]), _ZERO, 10, Point([1, 2, 3])),
        (Point([1, 2, 3]), Vector([1, 1, 1]), 10, Point([11, 12, 13])),
    ],
)
def test_at(origin, direction, magnitude, result):
    x = Ray(origin, direction).at(magnitude) == result
    assert x.all()
