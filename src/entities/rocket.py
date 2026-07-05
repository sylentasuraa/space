import pygame


class Rocket:
    x: float
    y: float

    width: int
    height: int

    body_color: tuple
    nose_color: tuple
    fin_color: tuple

    def __init__(self, x: float, y: float):
        ...

    def draw(self, surface: pygame.Surface):
        ...
