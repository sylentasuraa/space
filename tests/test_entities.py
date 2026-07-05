from entities.rocket import Rocket


def test_rocket_position():
    rocket = Rocket(100, 200)

    assert rocket.x == 100
    assert rocket.y == 200
