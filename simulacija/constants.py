"""
constants.py

Physical constants used throughout the Measurable Science project.

All values use SI units unless the unit is explicitly written
in the variable name.

No calculations are performed in this file.
"""

import numpy as np


# ============================================================
# Mathematical constants
# ============================================================

PI = np.pi

TWO_PI = 2.0 * PI

HALF_PI = PI / 2.0

DEGREES_TO_RADIANS = PI / 180.0

RADIANS_TO_DEGREES = 180.0 / PI


# ============================================================
# Time
# ============================================================

SECONDS_PER_MINUTE = 60.0

MINUTES_PER_HOUR = 60.0

HOURS_PER_DAY = 24.0

SECONDS_PER_HOUR = SECONDS_PER_MINUTE * MINUTES_PER_HOUR

SECONDS_PER_DAY = SECONDS_PER_HOUR * HOURS_PER_DAY


# ============================================================
# Earth
# ============================================================

EARTH_RADIUS_KM = 6371.0

EARTH_SIDEREAL_DAY_SECONDS = 86164.0905


# ============================================================
# Moon
# ============================================================

MOON_RADIUS_KM = 1737.4

AVERAGE_EARTH_MOON_DISTANCE_KM = 384400.0

MOON_SIDEREAL_PERIOD_DAYS = 27.321661