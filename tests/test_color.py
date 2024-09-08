from raytracer.color import write_color
import io

from raytracer.definitions import Color, Vector


def test_color():
    out = io.StringIO()
    write_color(out, Color(Vector([0, 0.1, 1.0])))
    assert out.getvalue() == "0 25 255\n"
