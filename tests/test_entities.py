import pygame

from entities.rocket import Rocket


def test_rocket_starts_at_given_position():
    rocket = Rocket(
        pygame.Vector2(100, 200)
    )

    assert rocket.position.x == 100
    assert rocket.position.y == 200


def test_apply_force_and_integrate_changes_velocity():
    rocket = Rocket(
        pygame.Vector2(0, 0)
    )

    rocket.mass = 2.0

    rocket.apply_force(
        pygame.Vector2(10, 0)
    )

    rocket.integrate(dt=1.0)

    assert rocket.velocity.x == 5


def test_force_accumulator_resets_after_integrate():
    rocket = Rocket(
        pygame.Vector2(0, 0)
    )

    rocket.apply_force(
        pygame.Vector2(10, 5)
    )

    rocket.integrate(dt=1.0)

    assert rocket.force_accum == pygame.Vector2(
        0,
        0,
    )


def test_zero_force_gives_constant_velocity_drift():
    rocket = Rocket(
        pygame.Vector2(0, 0)
    )

    rocket.apply_force(
        pygame.Vector2(10, 0)
    )

    rocket.integrate(dt=1.0)

    velocity_before = rocket.velocity.copy()

    rocket.integrate(dt=1.0)

    assert rocket.velocity == velocity_before