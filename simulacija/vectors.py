"""
vectors.py

Basic 3D vector mathematics used throughout the project.

This module intentionally contains no astronomy.

Every vector represents a physical quantity.

Examples:

earth_to_moon
observer_to_moon
moon_velocity
earth_rotation_axis
"""

from __future__ import annotations

from dataclasses import dataclass
import numpy as np


EPSILON = 1.0e-12


@dataclass(slots=True)
class Vector3:
    """
    Three-dimensional vector.

    Components are stored as floating-point numbers.

    Units are not enforced.
    The variable name must describe the physical meaning.

    Examples
    --------
    earth_to_moon
    observer_to_moon
    moon_velocity
    """

    x: float
    y: float
    z: float

    @classmethod
    def from_numpy(cls, values: np.ndarray) -> "Vector3":
        """Create a Vector3 from a NumPy array."""
        return cls(float(values[0]), float(values[1]), float(values[2]))

    def to_numpy(self) -> np.ndarray:
        """Return the vector as a NumPy array."""
        return np.array([self.x, self.y, self.z], dtype=float)

    def length(self) -> float:
        """
        Euclidean vector length.

        |v| = sqrt(x²+y²+z²)
        """
        return float(np.linalg.norm(self.to_numpy()))

    def normalize(self) -> "Vector3":
        """
        Return a unit vector.

        v̂ = v / |v|
        """
        magnitude = self.length()

        if magnitude < EPSILON:
            raise ValueError("Cannot normalize a zero-length vector.")

        return self / magnitude

    def dot(self, other: "Vector3") -> float:
        """
        Scalar product.

        a·b = axbx + ayby + azbz
        """
        return float(np.dot(self.to_numpy(), other.to_numpy()))

    def cross(self, other: "Vector3") -> "Vector3":
        """
        Vector product.

        Right-hand rule.
        """
        return Vector3.from_numpy(
            np.cross(self.to_numpy(), other.to_numpy())
        )

    def angle_with(self, other: "Vector3") -> float:
        """
        Return the angle between two vectors.

        Result is in radians.
        """
        a = self.normalize()
        b = other.normalize()

        cosine = np.clip(a.dot(b), -1.0, 1.0)

        return float(np.arccos(cosine))

    def project_onto(self, other: "Vector3") -> "Vector3":
        """
        Orthogonal projection onto another vector.
        """
        unit = other.normalize()

        return unit * self.dot(unit)

    def reject_from(self, other: "Vector3") -> "Vector3":
        """
        Component perpendicular to another vector.
        """
        return self - self.project_onto(other)

    def __add__(self, other: "Vector3") -> "Vector3":
        return Vector3(
            self.x + other.x,
            self.y + other.y,
            self.z + other.z,
        )

    def __sub__(self, other: "Vector3") -> "Vector3":
        return Vector3(
            self.x - other.x,
            self.y - other.y,
            self.z - other.z,
        )

    def __mul__(self, value: float) -> "Vector3":
        return Vector3(
            self.x * value,
            self.y * value,
            self.z * value,
        )

    def __truediv__(self, value: float) -> "Vector3":
        return Vector3(
            self.x / value,
            self.y / value,
            self.z / value,
        )

    def __neg__(self) -> "Vector3":
        return Vector3(
            -self.x,
            -self.y,
            -self.z,
        )

    def __repr__(self) -> str:
        return (
            f"Vector3("
            f"x={self.x:.6f}, "
            f"y={self.y:.6f}, "
            f"z={self.z:.6f})"
        )