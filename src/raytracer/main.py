"""
This is a skeleton file that can serve as a starting point for a Python
console script. To run this script uncomment the following lines in the
``[options.entry_points]`` section in ``setup.cfg``::

    console_scripts =
         fibonacci = raytracer.skeleton:run

Then run ``pip install .`` (or ``pip install -e .`` for editable mode)
which will install the command ``fibonacci`` inside your current environment.

Besides console scripts, the header (i.e. until ``_logger``...) of this file can
also be used as template for Python modules.

Note:
    This file can be renamed depending on your needs or safely removed if not needed.

References:
    - https://setuptools.pypa.io/en/latest/userguide/entry_point.html
    - https://pip.pypa.io/en/stable/reference/pip_install
"""

import io
import logging
import sys
from typing import Final

from tqdm import trange
from tqdm.contrib.logging import logging_redirect_tqdm

from raytracer import color
from raytracer.definitions import Color, Point, Vector
from raytracer.ray import Ray

_logger = logging.getLogger(__name__)

__author__ = "lehaas"
__copyright__ = "lehaas"
__license__ = "MIT"

ASPECT_RATIO: Final = 16.0 / 9.0
IMAGE_W: Final = 200


def output_ppm_image(output: io.StringIO) -> None:
    IMAGE_H: Final = 256
    IMAGE_W: Final = 256

    """Output a simple ppm image."""
    output.write("P3\n")
    output.write(f"{IMAGE_W} {IMAGE_H}\n")
    output.write("255\n")

    with logging_redirect_tqdm():
        for i in trange(IMAGE_H):
            for j in range(IMAGE_W):
                pixel_color = Color(
                    [float(j) / (IMAGE_W - 1), float(i) / (IMAGE_H - 1), 0.0]
                )

                color.write_color(output, pixel_color)

    _logger.info("Done.")


def simple_main():
    # TODO: to enable the console_script, a callable needs to be provided.
    # but having the logging config in a method is great in case main gets called multiple times.
    logging.basicConfig(level=logging.INFO)

    output = io.StringIO()
    output_ppm_image(sys.stdout)
    output.close()


def main():
    logging.basicConfig(level=logging.INFO)

    output = sys.stdout

    # Image properties
    image_width = IMAGE_W
    image_height = int(image_width / ASPECT_RATIO)

    assert image_height >= 1

    # Camera
    focal_length = 1.0
    viewport_height = 2.0
    viewport_width = viewport_height * image_width / image_height
    camera_center = Point([0, 0, 0])
    _logger.debug(f"{viewport_height=} {viewport_width=}")

    # Calculate viewport vectors along horizontal and vertical edges
    viewport_u = Vector([viewport_width, 0, 0])
    viewport_v = Vector([0, -viewport_height, 0])

    # Calculate viewport pixel distances
    pixel_delta_u = viewport_u / image_width
    pixel_delta_v = viewport_v / image_height
    _logger.debug(f"{pixel_delta_u=}, {pixel_delta_v=}")

    # Calculate location of the upper_left pixel
    viewport_upper_left = (
        camera_center - Vector([0, 0, focal_length]) - viewport_u / 2 - viewport_v / 2
    )
    pixel_00_loc = viewport_upper_left + 0.5 * (pixel_delta_u + pixel_delta_v)
    _logger.debug(f"{viewport_upper_left=}, {pixel_00_loc=}")

    output.write("P3\n")
    output.write(f"{image_width} {image_height}\n")
    output.write("255\n")

    with logging_redirect_tqdm():
        for j in trange(image_height):
            for i in range(image_width):
                pixel_center = pixel_00_loc + (i * pixel_delta_u) + (j * pixel_delta_v)
                ray_direction = pixel_center - camera_center
                r = Ray(camera_center, ray_direction)
                c = color.color_ray(r)

                _logger.debug(f"{i=} {j=} {ray_direction=}, {c=}")

                color.write_color(output, c)

    _logger.info("Done.")


if __name__ == "__main__":
    main()
