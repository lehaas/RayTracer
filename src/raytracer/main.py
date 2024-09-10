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

import logging
import sys
from typing import Final


from raytracer.definitions.vector import Point, Vector
from raytracer.definitions.world import World
from raytracer.hitable import Sphere
from raytracer.raytracer import RayTracer

_logger = logging.getLogger(__name__)

__author__ = "lehaas"
__copyright__ = "lehaas"
__license__ = "MIT"

ASPECT_RATIO: Final = 16.0 / 9.0
IMAGE_W: Final = 400


# def output_ppm_image(output: io.StringIO) -> None:
#     IMAGE_H: Final = 256
#     IMAGE_W: Final = 256

#     """Output a simple ppm image."""
#     output.write("P3\n")
#     output.write(f"{IMAGE_W} {IMAGE_H}\n")
#     output.write("255\n")

#     with logging_redirect_tqdm():
#         for i in trange(IMAGE_H):
#             for j in range(IMAGE_W):
#                 pixel_color = Color(
#                     [float(j) / (IMAGE_W - 1), float(i) / (IMAGE_H - 1), 0.0]
#                 )

#                 color.write_color(output, pixel_color)

#     _logger.info("Done.")


# def simple_main():
#     # TODO: to enable the console_script, a callable needs to be provided.
#     # but having the logging config in a method is great in case main gets called multiple times.
#     logging.basicConfig(level=logging.INFO)

#     output = io.StringIO()
#     output_ppm_image(sys.stdout)
#     output.close()


def main():
    logging.basicConfig(level=logging.INFO)

    world = (
        World()
        .add(Sphere(Point(Vector([0, 0, -1])), 0.5))
        .add(Sphere(Point(Vector([0, -100.5, -1])), 100))
    )

    output = sys.stdout

    # Image properties
    RayTracer(ASPECT_RATIO, IMAGE_W).render(world, output)

    _logger.info("Done.")


if __name__ == "__main__":
    main()
