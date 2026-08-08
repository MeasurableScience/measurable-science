"""
time_system.py

Astronomical time system used throughout the Measurable Science project.

All astronomical calculations use Julian Day internally.

Reference
---------
Jean Meeus
Astronomical Algorithms
Second Edition
Chapter 7
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
import math

from constants import (
    DEGREES_TO_RADIANS,
    TWO_PI,
)


# ============================================================
# Julian Date
# ============================================================


@dataclass(slots=True)
class JulianDate:
    """
    Astronomical Julian Day.

    Example
    -------
    JD = 2451545.0

    corresponds to

    2000-01-01 12:00 UTC
    """

    value: float

    def centuries_since_j2000(self) -> float:
        """
        Julian centuries since J2000.0

        T = (JD - 2451545.0) / 36525
        """

        return (self.value - 2451545.0) / 36525.0


# ============================================================
# Time conversion
# ============================================================


def utc_to_julian_day(
    utc_time: datetime,
) -> JulianDate:
    """
    Convert UTC datetime to Julian Day.

    Reference
    ---------
    Meeus Chapter 7
    """

    if utc_time.tzinfo is None:
        raise ValueError(
            "datetime must contain timezone information."
        )

    utc_time = utc_time.astimezone(timezone.utc)

    year = utc_time.year
    month = utc_time.month

    day = (
        utc_time.day
        + utc_time.hour / 24.0
        + utc_time.minute / 1440.0
        + utc_time.second / 86400.0
        + utc_time.microsecond / 86400.0e6
    )

    if month <= 2:
        year -= 1
        month += 12

    A = int(year / 100)
    B = 2 - A + int(A / 4)

    jd = (
        int(365.25 * (year + 4716))
        + int(30.6001 * (month + 1))
        + day
        + B
        - 1524.5
    )

    return JulianDate(jd)


# ============================================================
# Sidereal time
# ============================================================


def greenwich_mean_sidereal_time(
    jd: JulianDate,
) -> float:
    """
    Greenwich Mean Sidereal Time.

    Returns
    -------
    radians
    """

    T = jd.centuries_since_j2000()

    theta_deg = (
        280.46061837
        + 360.98564736629 * (jd.value - 2451545.0)
        + 0.000387933 * T * T
        - T * T * T / 38710000.0
    )

    theta_deg = theta_deg % 360.0

    return theta_deg * DEGREES_TO_RADIANS


def local_sidereal_time(
    jd: JulianDate,
    observer_longitude_rad: float,
) -> float:
    """
    Local Sidereal Time.

    Parameters
    ----------
    observer_longitude_rad

    East positive.

    Returns
    -------
    radians
    """

    lst = (
        greenwich_mean_sidereal_time(jd)
        + observer_longitude_rad
    )

    return lst % TWO_PI