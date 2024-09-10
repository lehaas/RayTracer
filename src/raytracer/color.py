import io


from raytracer.definitions.vector import Color


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
