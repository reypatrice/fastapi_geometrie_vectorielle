import pytest
from geometry import points


def test_distance():
    assert points.distance([0, 0], [3, 4]) == 5.0


def test_midpoint():
    assert points.midpoint([0, 0], [4, 6]) == [2.0, 3.0]


def test_centroid():
    assert points.centroid([[0, 0], [3, 0], [0, 3]]) == pytest.approx([1.0, 1.0])


def test_centroid_empty_raises():
    with pytest.raises(ValueError):
        points.centroid([])
