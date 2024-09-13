import io
import logging
import math
import random
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
    def __init__(
        self,
        aspect_ratio: float,
        image_width: int,
        samples_per_pixel: int = 40,
        max_recursion_depth: int = 20,
    ):
        """Compute a image with given aspect ratio and image_width.

        Args:
            aspect_raito: aspect ratio of the resulting image.
            image_width: width of the computed image
            samples_per_pixel: Number of rays to compute per pixel.
            max_recursion_depth: Maximum number of refections considered for diffuse materials.
        """
        self.aspect_ratio = aspect_ratio
        self.image_width = image_width
        self.image_height = int(self.image_width / self.aspect_ratio)
        self.samples_per_pixel = samples_per_pixel
        self.max_recursion_depth = max_recursion_depth

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
            color = sum(
                ray_color(self.sample_ray(i, j), world, depth=self.max_recursion_depth)
                for _ in range(self.samples_per_pixel)
            )
            return color / self.samples_per_pixel

        output_ppm(output, self.image_height, self.image_width, compute_color)

    def sample_ray(self, i, j):
        """Sample a ray centered at i, j with a random offset in [-0.5, -0.5, 0] and [0.5, 0.5, 0]."""
        offset = sample_square()
        pixel_center = (
            self.pixel_00_loc
            + ((i + offset.x) * self.pixel_delta_u)
            + ((j + offset.y) * self.pixel_delta_v)
        )
        ray_origin = self.camera.center
        ray_direction = pixel_center - ray_origin

        return Ray(ray_origin, ray_direction)


WHITE = Color(Vector([1.0, 1.0, 1.0]))
BLUE = Color(Vector([0.5, 0.7, 1.0]))


def sample_square() -> Vector:
    """Return a random vector to a point in the [-.5, -.5, 0] and [.5, .5, 0] unit square."""
    return Vector([random.random() - 0.5, random.random() - 0.5, 0])


def ray_color(ray: Ray, world: World, *, depth: int) -> Color:
    if depth == 0:
        return Color(Vector([0.0, 0.0, 0.0]))

    # to account for floating point inaccuracies, we ignore small rays that hit its origin
    if record := world.hit(ray, 0.0001, math.inf):
        # v is in [-1, 1]: scale it to [0, 1]
        # TODO: Vector should not be required here, but mypy cannot infer the type of 0.5*(v + 1)

        # cheap true Lambertian reflection
        direction = record.normal + Vector.random_unit_vector()

        # random reflection
        # direction = Vector.random_on_hemisphere(record.normal)

        return 0.5 * ray_color(Ray(record.point, direction), world, depth=depth - 1)

    v = unit_vector(ray.direction)
    a = 0.5 * (v.y + 1.0)
    return (1.0 - a) * WHITE + a * BLUE
