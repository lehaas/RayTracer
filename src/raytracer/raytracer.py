import io
import logging
import math
from typing import Callable

from tqdm import trange
from tqdm.contrib.logging import logging_redirect_tqdm

from raytracer.color import write_color
from raytracer.definitions.camera import Camera
from raytracer.definitions.vector import Color, Point, Vector, unit_vector
from raytracer.definitions.ray import Ray
from raytracer.definitions.world import World

_logger = logging.getLogger(__name__)


def output_ppm(
    output: io.StringIO, height: int, width: int, func: Callable[[int, int], Color]
) -> None:
    """Write a valid ppm to output applying func to compute every pixel color.

    TODO:
    - make write_color injectable to ease testing.
    """

    output.write("P3\n")
    output.write(f"{width} {height}\n")
    output.write("255\n")

    with logging_redirect_tqdm():
        for r in trange(height):
            for c in range(width):
                color = func(c, r)
                _logger.debug(f"{c=} {r=}: {color=}")

                write_color(output, color)


class RayTracer:
    def __init__(self, aspect_ratio: float, image_width: int):
        self.aspect_ratio = aspect_ratio
        self.image_width = image_width
        self.image_height = int(self.image_width / self.aspect_ratio)

        assert self.image_height >= 1

    def initialize(self):
        # Camera
        viewport_height = 2.0
        camera = Camera(
            focal_length=1.0,
            viewport_height=viewport_height,
            viewport_width=viewport_height * self.image_width / self.image_height,
            center=Point(Vector([0, 0, 0])),
        )
        _logger.debug(f"{camera=}")

        # Calculate viewport pixel distances
        pixel_delta_u = camera.viewport_u / self.image_width
        pixel_delta_v = camera.viewport_v / self.image_height
        _logger.debug(f"{pixel_delta_u=}, {pixel_delta_v=}")

        # Calculate location of the upper_left pixel
        pixel_00_loc = camera.viewport_upper_left + 0.5 * (
            pixel_delta_u + pixel_delta_v
        )
        _logger.debug(f"{camera.viewport_upper_left=}, {pixel_00_loc=}")

        self.camera = camera
        self.pixel_00_loc = pixel_00_loc
        self.pixel_delta_u = pixel_delta_u
        self.pixel_delta_v = pixel_delta_v

    def render(self, world: World, output: io.StringIO):
        self.initialize()

        def compute_color(i, j):
            pixel_center = (
                self.pixel_00_loc + (i * self.pixel_delta_u) + (j * self.pixel_delta_v)
            )
            ray_direction = pixel_center - self.camera.center
            r = Ray(self.camera.center, ray_direction)
            return ray_color(r, world)

        output_ppm(output, self.image_height, self.image_width, compute_color)


WHITE = Color(Vector([1.0, 1.0, 1.0]))
BLUE = Color(Vector([0.5, 0.7, 1.0]))


def ray_color(ray: Ray, world: World) -> Color:
    if record := world.hit(ray, 0, math.inf):
        # v is in [-1, 1]: scale it to [0, 1]
        # TODO: Vector should not be required here, but mypy cannot infer the type of 0.5*(v + 1)
        return Color(Vector((record.normal + 1) * 0.5))

    v = unit_vector(ray.direction)
    a = 0.5 * (v.y + 1.0)
    return (1.0 - a) * WHITE + a * BLUE
