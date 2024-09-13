import io

import numpy as np


from raytracer.definitions.vector import Color


X_MAX = 0.9999
X_MIN = 0.0000
MAX_BYTE = 256


def linear_to_gamma(linear_comp: float) -> float:
    if linear_comp > 0:
        return np.sqrt(linear_comp)
    return 0


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

    r = linear_to_gamma(r)
    g = linear_to_gamma(g)
    b = linear_to_gamma(b)

    r_byte = int(MAX_BYTE * clamp(r, X_MIN, X_MAX))
    g_byte = int(MAX_BYTE * clamp(g, X_MIN, X_MAX))
    b_byte = int(MAX_BYTE * clamp(b, X_MIN, X_MAX))

    out.write(f"{r_byte} {g_byte} {b_byte}\n")


def clamp(x: float, x_min: float, x_max: float) -> float:
    return max(min(x, x_max), x_min)
