from raytracer.definitions.vector import Point, Vector


class Ray:
    def __init__(self, origin: Point, direction: Vector) -> None:
        self.orig = origin
        self.direction = direction

    def at(self, t: float) -> Point:
        return self.orig + t * self.direction
