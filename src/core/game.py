import pygame

from entities.rocket import Rocket
from entities.ground import Ground
from entities.celestial_body import CelestialBody

from physics.gravity import (
    compute_gravity_force,
)

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

        self.screen = pygame.display.set_mode(
            (WIDTH, HEIGHT)
        )

        pygame.display.set_caption(
            "Orbital Simulator"
        )

        self.clock = pygame.time.Clock()
        self.running = True

        self.G = 5000

        self.ground = Ground(
            GROUND_HEIGHT,
            GROUND_COLOR,
        )

        self.planet = CelestialBody(
            position=pygame.Vector2(
                WIDTH / 2,
                HEIGHT / 2,
            ),
            mass=10000,
            radius=40,
        )

        self.rocket = Rocket(
            position=pygame.Vector2(
                WIDTH / 2 + 250,
                HEIGHT / 2,
            ),
            mass=10,
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

    def update(
        self,
        dt: float,
    ):
        gravity_force = (
            compute_gravity_force(
                self.planet,
                self.rocket,
                self.G,
            )
        )

        self.rocket.apply_force(
            gravity_force
        )

        self.rocket.integrate(dt)

    def render(self):
        self.screen.fill(
            BACKGROUND_COLOR
        )

        self.planet.draw(
            self.screen
        )

        self.rocket.draw(
            self.screen
        )

        pygame.display.flip()