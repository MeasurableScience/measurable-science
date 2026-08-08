"""
Unit tests for vectors.py
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

import math

from vectors import Vector3


def test_length():

    earth_to_moon = Vector3(
        3.0,
        4.0,
        0.0,
    )

    assert math.isclose(
        earth_to_moon.length(),
        5.0,
        rel_tol=1e-12,
    )


def test_normalize():

    earth_to_moon = Vector3(
        0.0,
        0.0,
        10.0,
    )

    direction = earth_to_moon.normalize()

    assert math.isclose(direction.x, 0.0)
    assert math.isclose(direction.y, 0.0)
    assert math.isclose(direction.z, 1.0)


def test_dot_product():

    earth_to_moon = Vector3(
        1.0,
        0.0,
        0.0,
    )

    earth_rotation_axis = Vector3(
        0.0,
        1.0,
        0.0,
    )

    assert math.isclose(
        earth_to_moon.dot(
            earth_rotation_axis
        ),
        0.0,
    )


def test_cross_product():

    x_axis = Vector3(
        1.0,
        0.0,
        0.0,
    )

    y_axis = Vector3(
        0.0,
        1.0,
        0.0,
    )

    z_axis = x_axis.cross(y_axis)

    assert math.isclose(z_axis.x, 0.0)
    assert math.isclose(z_axis.y, 0.0)
    assert math.isclose(z_axis.z, 1.0)


def test_projection():

    earth_to_moon = Vector3(
        2.0,
        2.0,
        0.0,
    )

    x_axis = Vector3(
        1.0,
        0.0,
        0.0,
    )

    projection = earth_to_moon.project_onto(
        x_axis
    )

    assert math.isclose(projection.x, 2.0)
    assert math.isclose(projection.y, 0.0)
    assert math.isclose(projection.z, 0.0)


if __name__ == "__main__":

    test_length()

    test_normalize()

    test_dot_product()

    test_cross_product()

    test_projection()

    print("All vector tests passed.")