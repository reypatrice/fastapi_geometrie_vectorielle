"""Droites, segments et polygones : la géométrie « appliquée ».
Comment l'algèbre des vecteurs (produit scalaire, produit vectoriel) résout des
problèmes concrets : de quel côté d'une droite est un point, deux segments se
croisent-ils, quelle est l'aire d'un polygone, un point est-il dedans, etc.
"""
import numpy as np


def orientation(a, b, c):
    """Position de c par rapport à la droite orientée (a -> b).

    +1 si c est à gauche (sens trigonométrique), -1 à droite, 0 si alignés.
    C'est le signe du produit vectoriel 2D de (b - a) et (c - a).
    """
    a, b, c = (np.asarray(p, dtype=float) for p in (a, b, c))
    cross = (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])
    if cross > 1e-12:
        return 1
    if cross < -1e-12:
        return -1
    return 0


def collinear(a, b, c):
    """Vrai si les trois points sont alignés."""
    return orientation(a, b, c) == 0


def point_line_distance(p, a, b):
    """Distance d'un point à la droite infinie passant par a et b."""
    p, a, b = (np.asarray(x, dtype=float) for x in (p, a, b))
    ab = b - a
    length = np.linalg.norm(ab)
    if length == 0:
        raise ValueError("a et b doivent être distincts pour définir une droite.")
    cross = ab[0] * (p[1] - a[1]) - ab[1] * (p[0] - a[0])
    return float(abs(cross) / length)


def point_segment_distance(p, a, b):
    """Distance d'un point au segment [a, b] (borné, contrairement à la droite)."""
    p, a, b = (np.asarray(x, dtype=float) for x in (p, a, b))
    ab = b - a
    denom = np.dot(ab, ab)
    if denom == 0:
        return float(np.linalg.norm(p - a))
    t = np.clip(np.dot(p - a, ab) / denom, 0.0, 1.0)
    closest = a + t * ab
    return float(np.linalg.norm(p - closest))


def segment_intersection(p1, p2, p3, p4):
    """Point d'intersection des segments [p1, p2] et [p3, p4], ou None."""
    p1, p2, p3, p4 = (np.asarray(x, dtype=float) for x in (p1, p2, p3, p4))
    r = p2 - p1
    s = p4 - p3
    denom = r[0] * s[1] - r[1] * s[0]
    if abs(denom) < 1e-12:
        return None  # parallèles ou colinéaires
    qp = p3 - p1
    t = (qp[0] * s[1] - qp[1] * s[0]) / denom
    u = (qp[0] * r[1] - qp[1] * r[0]) / denom
    if 0.0 <= t <= 1.0 and 0.0 <= u <= 1.0:
        return (p1 + t * r).tolist()
    return None


def polygon_area(points):
    """Aire signée d'un polygone (formule du lacet). Positive en sens trigo."""
    pts = np.asarray(points, dtype=float)
    if len(pts) < 3:
        raise ValueError("Un polygone exige au moins trois sommets.")
    x, y = pts[:, 0], pts[:, 1]
    return float(0.5 * np.sum(x * np.roll(y, -1) - np.roll(x, -1) * y))


def polygon_perimeter(points):
    """Périmètre d'un polygone fermé."""
    pts = np.asarray(points, dtype=float)
    rolled = np.roll(pts, -1, axis=0)
    return float(np.sum(np.linalg.norm(rolled - pts, axis=1)))


def polygon_centroid(points):
    """Centroïde d'un polygone, pondéré par l'aire."""
    pts = np.asarray(points, dtype=float)
    x, y = pts[:, 0], pts[:, 1]
    cross = x * np.roll(y, -1) - np.roll(x, -1) * y
    area = 0.5 * np.sum(cross)
    if abs(area) < 1e-12:
        return pts.mean(axis=0).tolist()
    cx = np.sum((x + np.roll(x, -1)) * cross) / (6 * area)
    cy = np.sum((y + np.roll(y, -1)) * cross) / (6 * area)
    return [float(cx), float(cy)]


def point_in_polygon(p, points):
    """Vrai si le point est à l'intérieur du polygone (lancer de rayon)."""
    x, y = np.asarray(p, dtype=float)
    pts = np.asarray(points, dtype=float)
    inside = False
    n = len(pts)
    j = n - 1
    for i in range(n):
        xi, yi = pts[i]
        xj, yj = pts[j]
        if ((yi > y) != (yj > y)) and (x < (xj - xi) * (y - yi) / (yj - yi) + xi):
            inside = not inside
        j = i
    return bool(inside)


def is_convex(points):
    """Vrai si le polygone est convexe (tous les virages dans le même sens)."""
    pts = np.asarray(points, dtype=float)
    n = len(pts)
    if n < 3:
        raise ValueError("Un polygone exige au moins trois sommets.")
    signs = []
    for i in range(n):
        a, b, c = pts[i], pts[(i + 1) % n], pts[(i + 2) % n]
        o = orientation(a, b, c)
        if o != 0:
            signs.append(o)
    return all(s == signs[0] for s in signs) if signs else True