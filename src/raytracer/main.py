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
