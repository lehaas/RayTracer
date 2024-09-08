from raytracer.definitions import Point, Vector


class Ray:
    def __init__(self, origin: Point, direction: Vector) -> None:
        self.orig = origin
        self.dir = direction

    def at(self, t: float) -> Point:
        return self.orig + t * self.dir
