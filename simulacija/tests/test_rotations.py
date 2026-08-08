"""
Unit tests for vectors.py
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

import math

from vectors import Vector3

from rotations import (
    rotate_x,
    rotate_y,
    rotate_z,
)


def test_rotate_z():

    earth_to_moon = Vector3(
        1.0,
        0.0,
        0.0,
    )

    rotated = rotate_z(
        earth_to_moon,
        math.pi / 2,
    )

    assert math.isclose(rotated.x, 0.0, abs_tol=1e-12)
    assert math.isclose(rotated.y, 1.0, abs_tol=1e-12)
    assert math.isclose(rotated.z, 0.0, abs_tol=1e-12)


def test_rotate_x():

    vector = Vector3(
        0.0,
        1.0,
        0.0,
    )

    rotated = rotate_x(
        vector,
        math.pi / 2,
    )

    assert math.isclose(rotated.x, 0.0)
    assert math.isclose(rotated.y, 0.0, abs_tol=1e-12)
    assert math.isclose(rotated.z, 1.0, abs_tol=1e-12)


def test_rotate_y():

    vector = Vector3(
        0.0,
        0.0,
        1.0,
    )

    rotated = rotate_y(
        vector,
        math.pi / 2,
    )

    assert math.isclose(rotated.x, 1.0, abs_tol=1e-12)
    assert math.isclose(rotated.y, 0.0)
    assert math.isclose(rotated.z, 0.0, abs_tol=1e-12)


if __name__ == "__main__":

    test_rotate_x()

    test_rotate_y()

    test_rotate_z()

    print("All rotation tests passed.")