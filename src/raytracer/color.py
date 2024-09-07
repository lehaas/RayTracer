import io
import numpy as np


def write_color(out: io.StringIO, pixel_color: np.ndarray) -> None:
    """Write a color to the output."""
    r, g, b = pixel_color

    out.write(f"{int(255.999 * r)} {int(255.999 * g)} {int(255.999 * b)}\n")
