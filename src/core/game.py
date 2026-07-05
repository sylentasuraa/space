from entities.rocket import Rocket
from entities.ground import Ground


class Game:
    screen: object
    clock: object
    running: bool
    rocket: Rocket
    ground: Ground

    def __init__(self):
        ...

    def run(self):
        ...

    def handle_events(self):
        ...

    def update(self, dt: float):
        ...

    def render(self):
        ...
