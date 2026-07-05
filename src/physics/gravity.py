from pygame import Vector2


def compute_gravity_force(
    body,
    rocket,
    G: float,
) -> Vector2:
    direction = (
        body.position
        - rocket.position
    )

    distance = direction.length()

    if distance == 0:
        return Vector2()

    direction_unit = (
        direction.normalize()
    )

    force_magnitude = (
        G
        * body.mass
        * rocket.mass
        / (distance ** 2)
    )

    return (
        direction_unit
        * force_magnitude
    )