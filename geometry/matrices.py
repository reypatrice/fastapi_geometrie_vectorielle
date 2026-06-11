"""Matrices de transformation 2D, en coordonnées homogènes (3x3).
On représente un point (x, y) par (x, y, 1) : toutes les transformations
affines deviennent des matrices 3x3 que l'on peut enchaîner par multiplication.
"""
import numpy as np


def identity():
    """Matrice identité (ne change rien)."""
    return np.eye(3).tolist()


def _translation(dx, dy):
    return np.array([[1, 0, dx],
                     [0, 1, dy],
                     [0, 0, 1]], dtype=float)


def translation(dx, dy):
    """Translation de (dx, dy)."""
    return _translation(dx, dy).tolist()


def rotation(angle_deg, center=(0.0, 0.0)):
    """Rotation (en degrés) autour d'un centre."""
    a = np.radians(angle_deg)
    c, s = np.cos(a), np.sin(a)
    rot = np.array([[c, -s, 0],
                    [s,  c, 0],
                    [0,  0, 1]], dtype=float)
    cx, cy = center
    # ramener le centre à l'origine, tourner, puis le remettre en place
    return (_translation(cx, cy) @ rot @ _translation(-cx, -cy)).tolist()


def scaling(sx, sy, center=(0.0, 0.0)):
    """Mise à l'échelle autour d'un centre."""
    scale = np.array([[sx, 0, 0],
                      [0, sy, 0],
                      [0,  0, 1]], dtype=float)
    cx, cy = center
    return (_translation(cx, cy) @ scale @ _translation(-cx, -cy)).tolist()


def shear(kx, ky):
    """Cisaillement : x' = x + kx*y, y' = y + ky*x."""
    return np.array([[1, kx, 0],
                     [ky, 1, 0],
                     [0,  0, 1]], dtype=float).tolist()


def reflection(angle_deg):
    """Réflexion par rapport à une droite passant par l'origine.
    angle_deg : angle de la droite avec l'axe des x
    (0° = axe des x, 90° = axe des y).
    """
    a = np.radians(2 * angle_deg)
    c, s = np.cos(a), np.sin(a)
    return np.array([[c,  s, 0],
                     [s, -c, 0],
                     [0,  0, 1]], dtype=float).tolist()


def multiply(matrices):
    """Compose plusieurs matrices en une seule (de gauche à droite).
    multiply([A, B]) = A @ B : appliquer le résultat revient à appliquer B,
    puis A.
    """
    result = np.eye(3)
    for matrix in matrices:
        result = result @ np.asarray(matrix, dtype=float)
    return result.tolist()


def invert(matrix):
    """Transformation réciproque. Lève ValueError si la matrice est singulière."""
    matrix = np.asarray(matrix, dtype=float)
    try:
        return np.linalg.inv(matrix).tolist()
    except np.linalg.LinAlgError:
        raise ValueError("Matrice non inversible (singulière).")


def apply(points, matrix):
    """Applique une matrice 3x3 à une liste de points 2D."""
    pts = np.asarray(points, dtype=float)
    matrix = np.asarray(matrix, dtype=float)
    if pts.ndim != 2 or pts.shape[1] != 2:
        raise ValueError("`points` doit être une liste de paires [x, y].")
    homogeneous = np.hstack([pts, np.ones((len(pts), 1))])
    transformed = (matrix @ homogeneous.T).T
    return transformed[:, :2].tolist()