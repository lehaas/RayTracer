import pytest
from raytracer.color import clamp, write_color
import io

from raytracer.definitions.vector import Color, Vector


def test_color(mocker):
    with mocker.patch("raytracer.color.linear_to_gamma", side_effect=lambda x: x):
        out = io.StringIO()
        write_color(out, Color(Vector([0, 0.1, 1.0])))
        assert out.getvalue() == "0 25 255\n"


@pytest.mark.parametrize(
    ("x", "res"), [(0.4, 0.4), (-1.0, 0.0), (1.0, 1.0), (1.2, 1.0), (0.0, 0.0)]
)
def test_clamp(x, res):
    x_min = 0.0
    x_max = 1.0

    assert clamp(x, x_min, x_max) == res
