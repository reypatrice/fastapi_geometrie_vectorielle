"""Opérations élémentaires sur les points 2D.

Conceptuellement, un *point* est une position dans le plan, tandis qu'un
vecteur est un déplacement. On garde donc ces opérations séparées de celles
du module vectors, même si la représentation [x, y] est identique.
"""
import numpy as np


def distance(p, q):
    """Distance euclidienne entre deux points."""
    return float(np.linalg.norm(np.asarray(q, dtype=float) - np.asarray(p, dtype=float)))


def midpoint(p, q):
    """Milieu du segment [p, q]."""
    return ((np.asarray(p, dtype=float) + np.asarray(q, dtype=float)) / 2.0).tolist()


def centroid(points):
    """Barycentre d'un nuage de points. Lève ValueError si la liste est vide."""
    pts = np.asarray(points, dtype=float)
    if len(pts) == 0:
        raise ValueError("Le barycentre exige au moins un point.")
    return pts.mean(axis=0).tolist()
