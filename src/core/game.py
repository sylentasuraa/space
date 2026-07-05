from entities.rocket import Rocket
from entities.ground import Ground

import pygame

from core.config import (
    WIDTH,
    HEIGHT,
    FPS,
    BACKGROUND_COLOR,
    GROUND_HEIGHT,
    GROUND_COLOR,
)


class Game:
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Orbital Simulator")

        self.clock = pygame.time.Clock()
        self.running = True

        self.ground = Ground(
            GROUND_HEIGHT,
            GROUND_COLOR,
        )

        rocket_x = WIDTH / 2
        rocket_y = HEIGHT - GROUND_HEIGHT

        self.rocket = Rocket(
            rocket_x,
            rocket_y,
        )

    def run(self):
        while self.running:
            dt = self.clock.tick(FPS) / 1000

            self.handle_events()
            self.update(dt)
            self.render()

        pygame.quit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def update(self, dt: float):
        # Physics and movement will go here later
        pass

    def render(self):
        self.screen.fill(BACKGROUND_COLOR)

        self.ground.draw(
            self.screen,
            WIDTH,
            HEIGHT,
        )

        self.rocket.draw(self.screen)

        pygame.display.flip()