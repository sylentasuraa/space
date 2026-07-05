from pygame import Vector2
import pygame


class CelestialBody:
    def __init__(
        self,
        position: Vector2,
        mass: float,
        radius: float,
        color=(0, 100, 255),
    ):
        self.position = position.copy()
        self.mass = mass
        self.radius = radius
        self.color = color

    def draw(
        self,
        surface,
    ):
        pygame.draw.circle(
            surface,
            self.color,
            (
                int(self.position.x),
                int(self.position.y),
            ),
            int(self.radius),
        )