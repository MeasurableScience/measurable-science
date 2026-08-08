"""
Unit tests for time_system.py
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

import math
from datetime import datetime
from datetime import timezone

from time_system import (
    utc_to_julian_day,
    local_sidereal_time,
)


def test_j2000():

    utc = datetime(
        2000,
        1,
        1,
        12,
        0,
        0,
        tzinfo=timezone.utc,
    )

    jd = utc_to_julian_day(
        utc
    )

    assert math.isclose(
        jd.value,
        2451545.0,
        rel_tol=1e-12,
    )


def test_local_sidereal_time():

    utc = datetime(
        2000,
        1,
        1,
        12,
        0,
        tzinfo=timezone.utc,
    )

    jd = utc_to_julian_day(
        utc
    )

    lst = local_sidereal_time(
        jd,
        0.0,
    )

    assert (
        0.0
        <= lst
        <= 2.0 * math.pi
    )


if __name__ == "__main__":

    test_j2000()

    test_local_sidereal_time()

    print("All time system tests passed.")