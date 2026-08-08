"""
rotations.py

Three-dimensional vector rotations.

This module contains only geometry.

No astronomy.
No physics.

All rotations follow the right-hand rule.
"""

from __future__ import annotations

import numpy as np

from vectors import Vector3


EPSILON = 1.0e-12


# ============================================================
# Rotation matrices
# ============================================================

def rotation_matrix_x(angle_rad: float) -> np.ndarray:
    """
    Rotation around the X axis.
    """

    c = np.cos(angle_rad)
    s = np.sin(angle_rad)

    return np.array([
        [1.0, 0.0, 0.0],
        [0.0, c, -s],
        [0.0, s, c],
    ])


def rotation_matrix_y(angle_rad: float) -> np.ndarray:
    """
    Rotation around the Y axis.
    """

    c = np.cos(angle_rad)
    s = np.sin(angle_rad)

    return np.array([
        [c, 0.0, s],
        [0.0, 1.0, 0.0],
        [-s, 0.0, c],
    ])


def rotation_matrix_z(angle_rad: float) -> np.ndarray:
    """
    Rotation around the Z axis.
    """

    c = np.cos(angle_rad)
    s = np.sin(angle_rad)

    return np.array([
        [c, -s, 0.0],
        [s,  c, 0.0],
        [0.0, 0.0, 1.0],
    ])


# ============================================================
# Generic rotation
# ============================================================

def rotate_about_axis(
    vector: Vector3,
    axis: Vector3,
    angle_rad: float,
) -> Vector3:
    """
    Rotate a vector around an arbitrary axis.

    Rodrigues' rotation formula

    v_rot =
        v cos(theta)
      + (k × v) sin(theta)
      + k (k·v)(1-cos(theta))

    where

        k = unit rotation axis
    """

    rotation_axis = axis.normalize()

    cosine = np.cos(angle_rad)
    sine = np.sin(angle_rad)

    term_1 = vector * cosine

    term_2 = rotation_axis.cross(vector) * sine

    term_3 = (
        rotation_axis
        * rotation_axis.dot(vector)
        * (1.0 - cosine)
    )

    return term_1 + term_2 + term_3


# ============================================================
# Convenience functions
# ============================================================

def rotate_x(
    vector: Vector3,
    angle_rad: float,
) -> Vector3:

    matrix = rotation_matrix_x(angle_rad)

    return Vector3.from_numpy(
        matrix @ vector.to_numpy()
    )


def rotate_y(
    vector: Vector3,
    angle_rad: float,
) -> Vector3:

    matrix = rotation_matrix_y(angle_rad)

    return Vector3.from_numpy(
        matrix @ vector.to_numpy()
    )


def rotate_z(
    vector: Vector3,
    angle_rad: float,
) -> Vector3:

    matrix = rotation_matrix_z(angle_rad)

    return Vector3.from_numpy(
        matrix @ vector.to_numpy()
    )