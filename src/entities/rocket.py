import pygame


class Rocket:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

        self.width = 40
        self.height = 100

        self.body_color = (200, 200, 200)
        self.nose_color = (150, 150, 150)
        self.fin_color = (100, 100, 100)

    def draw(self, surface: pygame.Surface):
        body_rect = pygame.Rect(
            self.x - self.width // 2,
            self.y - self.height,
            self.width,
            self.height,
        )

        pygame.draw.rect(
            surface,
            self.body_color,
            body_rect,
        )

        nose_points = [
            (self.x, self.y - self.height - 30),
            (self.x - self.width // 2, self.y - self.height),
            (self.x + self.width // 2, self.y - self.height),
        ]

        pygame.draw.polygon(
            surface,
            self.nose_color,
            nose_points,
        )

        left_fin = [
            (self.x - self.width // 2, self.y),
            (self.x - self.width // 2 - 20, self.y + 20),
            (self.x - self.width // 2, self.y - 20),
        ]

        right_fin = [
            (self.x + self.width // 2, self.y),
            (self.x + self.width // 2 + 20, self.y + 20),
            (self.x + self.width // 2, self.y - 20),
        ]

        pygame.draw.polygon(surface, self.fin_color, left_fin)
        pygame.draw.polygon(surface, self.fin_color, right_fin)