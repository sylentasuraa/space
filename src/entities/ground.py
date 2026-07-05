import pygame


class Ground:
    height: int
    color: tuple

    def __init__(self, height: int, color: tuple):
        ...

    def draw(
        self,
        surface: pygame.Surface,
        screen_width: int,
        screen_height: int
    ):
        ...
