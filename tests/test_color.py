from raytracer.color import write_color
import io

from raytracer.definitions import Color

__author__ = "lehaas"
__copyright__ = "lehaas"
__license__ = "MIT"


def test_color():
    out = io.StringIO()
    write_color(out, Color([0, 0.1, 1.0]))
    assert out.getvalue() == "0 25 255\n"
