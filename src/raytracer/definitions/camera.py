from dataclasses import dataclass
from raytracer.definitions.vector import Point, Vector


@dataclass
class Camera:
    focal_length: float
    viewport_height: float
    viewport_width: float
    center: Point

    @property
    def viewport_u(self) -> Vector:
        """Vector across the horizontal viewport edge."""
        return Vector([self.viewport_width, 0, 0])

    @property
    def viewport_v(self) -> Vector:
        """Vector down the left viewport edge."""
        return Vector([0, -self.viewport_height, 0])

    @property
    def viewport_upper_left(self) -> Vector:
        """Vector to the upper left viewport edge from the center."""
        return (
            self.center
            - Vector([0, 0, self.focal_length])
            - self.viewport_u / 2
            - self.viewport_v / 2
        )
