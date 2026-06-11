import pytest

from geometry import matrices


def test_identity_leaves_points_unchanged():
    assert matrices.apply([[2, 3]], matrices.identity()) == [[2.0, 3.0]]


def test_translation():
    m = matrices.translation(10, 5)
    assert matrices.apply([[0, 0], [1, 1]], m) == [[10.0, 5.0], [11.0, 6.0]]


def test_rotation_90():
    m = matrices.rotation(90)
    # apply renvoie une liste de points ; on extrait le point unique avec [0]
    # car pytest.approx n'accepte pas les listes imbriquées.
    assert matrices.apply([[1, 0]], m)[0] == pytest.approx([0.0, 1.0])


def test_scaling_keeps_center_fixed():
    m = matrices.scaling(2, 2, center=[1, 1])
    assert matrices.apply([[1, 1]], m)[0] == pytest.approx([1.0, 1.0])


def test_compose_two_translations():
    t1 = matrices.translation(1, 2)
    t2 = matrices.translation(3, 4)
    composed = matrices.multiply([t1, t2])
    assert matrices.apply([[0, 0]], composed)[0] == pytest.approx([4.0, 6.0])


def test_invert_singular_raises():
    singular = [[1, 1, 0], [1, 1, 0], [0, 0, 1]]
    with pytest.raises(ValueError):
        matrices.invert(singular)