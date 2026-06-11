import math
import pytest
from geometry import vectors

def test_add():
    assert vectors.add([1, 2], [3, 4]) == [4.0, 6.0]


def test_dot_orthogonal():
    assert vectors.dot([1, 0], [0, 1]) == 0.0


def test_norm():
    assert vectors.norm([3, 4]) == 5.0


def test_cross():
    assert vectors.cross([1, 0], [0, 1]) == 1.0


def test_normalize():
    # pytest.approx : compare des flottants en tolérant les arrondis.
    assert vectors.normalize([3, 4]) == pytest.approx([0.6, 0.8])


def test_normalize_zero_raises():
    # pytest.raises : vérifie qu'une exception est bien levée.
    with pytest.raises(ValueError):
        vectors.normalize([0, 0])


def test_angle_between_90_degrees():
    assert vectors.angle_between([1, 0], [0, 1]) == pytest.approx(math.pi / 2)


def test_project():
    assert vectors.project([3, 4], [1, 0]) == pytest.approx([3.0, 0.0])


def test_perpendicular():
    assert vectors.perpendicular([1, 0]) == [0.0, 1.0]


def test_lerp_midway():
    assert vectors.lerp([0, 0], [10, 20], 0.5) == [5.0, 10.0]