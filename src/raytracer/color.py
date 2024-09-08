import io


from raytracer.definitions import Color, Point, Vector, unit_vector
from raytracer.hitable import Sphere
from raytracer.ray import Ray


def write_color(out: io.StringIO, pixel_color: Color) -> None:
    """Write a color to the output.

    Args:
        out: output stream
        color: 3D vector of floats in [0,1].
    """
    assert 0.0 <= pixel_color[0] <= 1.0
    assert 0.0 <= pixel_color[1] <= 1.0
    assert 0.0 <= pixel_color[2] <= 1.0

    r, g, b = pixel_color

    out.write(f"{int(255.999 * r)} {int(255.999 * g)} {int(255.999 * b)}\n")


WHITE = Color(Vector([1.0, 1.0, 1.0]))
BLUE = Color(Vector([0.5, 0.7, 1.0]))


def color_ray(ray: Ray) -> Color:
    sphere = Sphere(Point(Vector([0, 0, -1])), 0.5)
    if record := sphere.hit(ray):
        v = unit_vector(record.normal)
        # v is in [-1, 1]: scale it to [0, 1]
        return Color(0.5 * (v + 1))

    v = unit_vector(ray.direction)
    a = 0.5 * (v.y + 1.0)
    return (1.0 - a) * WHITE + a * BLUE
