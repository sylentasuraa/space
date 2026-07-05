from pygame import Vector2

from entities.celestial_body import CelestialBody
from entities.rocket import Rocket
from physics.gravity import compute_gravity_force


def test_gravity_magnitude():
    G = 100.0

    planet = CelestialBody(
        position=Vector2(100, 0),
        mass=1000,
        radius=10,
    )

    rocket = Rocket(
        position=Vector2(0, 0),
        mass=10,
    )

    force = compute_gravity_force(
        planet,
        rocket,
        G,
    )

    expected = (
        G
        * planet.mass
        * rocket.mass
        / (100 ** 2)
    )

    assert abs(force.length() - expected) < 0.0001


def test_gravity_points_toward_planet():
    planet = CelestialBody(
        position=Vector2(100, 0),
        mass=1000,
        radius=10,
    )

    rocket = Rocket(
        position=Vector2(0, 0),
        mass=10,
    )

    force = compute_gravity_force(
        planet,
        rocket,
        100,
    )

    assert force.x > 0
    assert abs(force.y) < 0.0001


def test_gravity_stronger_when_closer():
    planet = CelestialBody(
        position=Vector2(100, 0),
        mass=1000,
        radius=10,
    )

    far_rocket = Rocket(
        position=Vector2(0, 0),
        mass=10,
    )

    close_rocket = Rocket(
        position=Vector2(50, 0),
        mass=10,
    )

    far_force = compute_gravity_force(
        planet,
        far_rocket,
        100,
    )

    close_force = compute_gravity_force(
        planet,
        close_rocket,
        100,
    )

    assert close_force.length() > far_force.length()
