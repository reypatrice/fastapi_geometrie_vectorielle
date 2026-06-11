import numpy as np


def add(a, b):
    """Somme de deux vecteurs : a + b."""
    return (np.asarray(a, dtype=float) + np.asarray(b, dtype=float)).tolist()


def dot(a, b):
    """Produit scalaire a · b."""
    return float(np.dot(np.asarray(a, dtype=float), np.asarray(b, dtype=float)))


def norm(v):
    """Norme (longueur) d'un vecteur."""
    return float(np.linalg.norm(np.asarray(v, dtype=float)))

def subtract(a, b):
    """Différence : a - b."""
    return (np.asarray(a, dtype=float) - np.asarray(b, dtype=float)).tolist()


def scale(v, k):
    """Multiplication par un scalaire : k * v."""
    return (np.asarray(v, dtype=float) * float(k)).tolist()


def linear_combination(a, b, alpha, beta):
    """Combinaison linéaire : alpha * a + beta * b."""
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    return (alpha * a + beta * b).tolist()


def cross(a, b):
    """Produit vectoriel 2D : composante z (scalaire).

    Son signe indique l'orientation de b par rapport à a.
    """
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    return float(a[0] * b[1] - a[1] * b[0])


def normalize(v):
    """Vecteur unitaire de même direction. Lève ValueError si v est nul."""
    v = np.asarray(v, dtype=float)
    n = np.linalg.norm(v)
    if n == 0:
        raise ValueError("Impossible de normaliser un vecteur nul.")
    return (v / n).tolist()


def heading(v):
    """Angle (radians) du vecteur par rapport à l'axe des x, via atan2."""
    v = np.asarray(v, dtype=float)
    return float(np.arctan2(v[1], v[0]))


def angle_between(a, b):
    """Angle (radians) entre deux vecteurs. Lève ValueError si l'un est nul."""
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    na, nb = np.linalg.norm(a), np.linalg.norm(b)
    if na == 0 or nb == 0:
        raise ValueError("Angle indéfini avec un vecteur nul.")
    cos_theta = np.clip(np.dot(a, b) / (na * nb), -1.0, 1.0)
    return float(np.arccos(cos_theta))


def project(a, b):
    """Projection orthogonale de a sur b. Lève ValueError si b est nul."""
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    bb = np.dot(b, b)
    if bb == 0:
        raise ValueError("Impossible de projeter sur un vecteur nul.")
    return (np.dot(a, b) / bb * b).tolist()


def perpendicular(v):
    """Vecteur perpendiculaire (rotation de +90°) : (x, y) -> (-y, x)."""
    v = np.asarray(v, dtype=float)
    return [float(-v[1]), float(v[0])]


def rotate(v, angle_rad):
    """Rotation d'un vecteur d'un angle (radians) autour de l'origine."""
    v = np.asarray(v, dtype=float)
    c, s = np.cos(angle_rad), np.sin(angle_rad)
    rotation = np.array([[c, -s], [s, c]], dtype=float)
    return (rotation @ v).tolist()


def lerp(a, b, t):
    """Interpolation linéaire : (1 - t) * a + t * b."""
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    return ((1.0 - t) * a + t * b).tolist()

