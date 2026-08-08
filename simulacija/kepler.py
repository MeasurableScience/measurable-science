"""
kepler.py

Numerical solution of Kepler's equation.

Reference
---------
Jean Meeus
Astronomical Algorithms

Kepler equation

M = E - e sin(E)
"""

from __future__ import annotations

import math

EPSILON = 1.0e-12
MAX_ITERATIONS = 25


def normalize_angle(angle_rad: float) -> float:
    """
    Normalize angle to [0, 2*pi).
    """
    return angle_rad % (2.0 * math.pi)


def solve_eccentric_anomaly(
    mean_anomaly_rad: float,
    eccentricity: float,
) -> float:
    """
    Solve Kepler's equation using Newton-Raphson iteration.

        M = E - e sin(E)

    Parameters
    ----------
    mean_anomaly_rad
        Mean anomaly in radians.

    eccentricity
        Orbital eccentricity.

    Returns
    -------
    Eccentric anomaly in radians.
    """

    mean_anomaly_rad = normalize_angle(mean_anomaly_rad)

    if eccentricity < 0.8:
        eccentric_anomaly = mean_anomaly_rad
    else:
        eccentric_anomaly = math.pi

    for _ in range(MAX_ITERATIONS):

        f = (
            eccentric_anomaly
            - eccentricity * math.sin(eccentric_anomaly)
            - mean_anomaly_rad
        )

        fp = (
            1.0
            - eccentricity * math.cos(eccentric_anomaly)
        )

        delta = f / fp

        eccentric_anomaly -= delta

        if abs(delta) < EPSILON:
            break

    return eccentric_anomaly


def eccentric_to_true_anomaly(
    eccentric_anomaly_rad: float,
    eccentricity: float,
) -> float:
    """
    Convert eccentric anomaly to true anomaly.
    """

    sin_v = (
        math.sqrt(1.0 - eccentricity ** 2)
        * math.sin(eccentric_anomaly_rad)
    )

    cos_v = (
        math.cos(eccentric_anomaly_rad)
        - eccentricity
    )

    return math.atan2(
        sin_v,
        cos_v,
    )


def orbital_radius(
    semi_major_axis_km: float,
    eccentricity: float,
    eccentric_anomaly_rad: float,
) -> float:
    """
    Distance from the focus.

        r = a (1 - e cos(E))
    """

    return (
        semi_major_axis_km
        * (
            1.0
            - eccentricity
            * math.cos(eccentric_anomaly_rad)
        )
    )