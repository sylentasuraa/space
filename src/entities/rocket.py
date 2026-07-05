import pygame


class Rocket:
    NOSE_LENGTH = 30
    FIN_SIZE = 20

    def __init__(self, position: pygame.Vector2):
        self.position = position.copy()

        self.velocity = pygame.Vector2(0, 0)
        self.force_accum = pygame.Vector2(0, 0)

        self.mass = 10.0

        self.width = 40
        self.height = 100

        self.body_color = (200, 200, 200)
        self.nose_color = (150, 150, 150)
        self.fin_color = (100, 100, 100)

    def apply_force(self, force: pygame.Vector2):
        self.force_accum += force

    def integrate(self, dt: float):
        acceleration = self.force_accum / self.mass

        self.velocity += acceleration * dt
        self.position += self.velocity * dt

        self.force_accum.update(0, 0)

    def draw(self, surface: pygame.Surface):
        x = self.position.x
        y = self.position.y

        body_rect = pygame.Rect(
            x - self.width // 2,
            y - self.height,
            self.width,
            self.height,
        )

        pygame.draw.rect(
            surface,
            self.body_color,
            body_rect,
        )

        nose_points = [
            (x, y - self.height - self.NOSE_LENGTH),
            (x - self.width // 2, y - self.height),
            (x + self.width // 2, y - self.height),
        ]

        pygame.draw.polygon(
            surface,
            self.nose_color,
            nose_points,
        )

        left_fin = [
            (x - self.width // 2, y),
            (x - self.width // 2 - self.FIN_SIZE, y + self.FIN_SIZE),
            (x - self.width // 2, y - self.FIN_SIZE),
        ]

        right_fin = [
            (x + self.width // 2, y),
            (x + self.width // 2 + self.FIN_SIZE, y + self.FIN_SIZE),
            (x + self.width // 2, y - self.FIN_SIZE),
        ]

        pygame.draw.polygon(
            surface,
            self.fin_color,
            left_fin,
        )

        pygame.draw.polygon(
            surface,
            self.fin_color,
            right_fin,
        )