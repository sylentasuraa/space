import pygame


class Ground:
    def __init__(self, height: int, color: tuple):
        self.height = height
        self.color = color

    def draw(
        self,
        surface: pygame.Surface,
        screen_width: int,
        screen_height: int
    ):
        pygame.draw.rect(
            surface,
            self.color,
            (
                0,
                screen_height - self.height,
                screen_width,
                self.height
            )
        )