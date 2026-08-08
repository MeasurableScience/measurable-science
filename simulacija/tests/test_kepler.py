"""
Unit tests for kepler.py
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

import math

from kepler import (
    solve_eccentric_anomaly,
    eccentric_to_true_anomaly,
    orbital_radius,
)


def test_circular_orbit():

    M = math.radians(45)

    E = solve_eccentric_anomaly(
        M,
        0.0,
    )

    assert math.isclose(
        E,
        M,
        rel_tol=1e-12,
    )


def test_true_anomaly():

    M = math.radians(90)

    E = solve_eccentric_anomaly(
        M,
        0.0549,
    )

    v = eccentric_to_true_anomaly(
        E,
        0.0549,
    )

    assert (
        0.0
        <= v
        <= 2.0 * math.pi
    )


def test_orbital_radius():

    a = 384400.0

    e = 0.0549

    E = 0.0

    r = orbital_radius(
        a,
        e,
        E,
    )

    expected = a * (1.0 - e)

    assert math.isclose(
        r,
        expected,
        rel_tol=1e-12,
    )


if __name__ == "__main__":

    test_circular_orbit()

    test_true_anomaly()

    test_orbital_radius()

    print("All Kepler tests passed.")