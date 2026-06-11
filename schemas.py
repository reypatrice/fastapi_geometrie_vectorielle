"""Modèles de données (Pydantic) partagés par tous les routers.

Centraliser ici les schémas d'entrée évite de les redéfinir dans chaque router
et offre un seul endroit où lire le « contrat » de l'API. Les alias de type
(Vec2, Matrix3, PointList) nomment l'intention sans rien changer au comportement.
"""
from typing import Annotated

from pydantic import BaseModel, Field

# --- Limites de taille (protection en usage public) -----------------------
# Plafonner la taille des entrées empêche qu'une requête démesurée
# (un polygone de plusieurs millions de points, par exemple) ne sature la
# mémoire du serveur. Au-delà de ces bornes, Pydantic renvoie tout seul un 422.
MAX_POINTS = 10_000      # nb max de points dans une figure / un polygone
MAX_MATRICES = 1_000     # nb max de matrices composées en une seule requête

Vec2 = Annotated[list[float], Field(min_length=2, max_length=2)]   # [x, y]
Matrix3 = list[list[float]]                                        # matrice 3x3
PointList = Annotated[list[list[float]], Field(max_length=MAX_POINTS)]


# --- Vecteurs -------------------------------------------------------------

class TwoVectors(BaseModel):
    a: Vec2
    b: Vec2


class OneVector(BaseModel):
    v: Vec2


class ScaleVector(BaseModel):
    v: Vec2
    k: float


class LinearCombination(BaseModel):
    a: Vec2
    b: Vec2
    alpha: float
    beta: float


class RotateVector(BaseModel):
    v: Vec2
    angle_rad: float


class Lerp(BaseModel):
    a: Vec2
    b: Vec2
    t: float


# --- Points ---------------------------------------------------------------

class TwoPoints(BaseModel):
    p: Vec2
    q: Vec2


class PointCloud(BaseModel):
    points: PointList


# --- Matrices -------------------------------------------------------------

class RotationParams(BaseModel):
    angle_deg: float
    center: Vec2 = [0.0, 0.0]


class ScalingParams(BaseModel):
    sx: float
    sy: float
    center: Vec2 = [0.0, 0.0]


class TranslationParams(BaseModel):
    dx: float
    dy: float


class ShearParams(BaseModel):
    kx: float = 0.0
    ky: float = 0.0


class ReflectionParams(BaseModel):
    angle_deg: float


class MatrixList(BaseModel):
    matrices: Annotated[list[Matrix3], Field(max_length=MAX_MATRICES)]


class OneMatrix(BaseModel):
    matrix: Matrix3


class ApplyMatrix(BaseModel):
    points: PointList
    matrix: Matrix3


class RotateFigure(BaseModel):
    points: PointList
    angle_deg: float
    center: Vec2 = [0.0, 0.0]


class ScaleFigure(BaseModel):
    points: PointList
    sx: float
    sy: float
    center: Vec2 = [0.0, 0.0]


class TranslateFigure(BaseModel):
    points: PointList
    dx: float
    dy: float


# --- Formes ---------------------------------------------------------------

class ThreePoints(BaseModel):
    a: Vec2
    b: Vec2
    c: Vec2


class PointAndSegment(BaseModel):
    p: Vec2
    a: Vec2
    b: Vec2


class TwoSegments(BaseModel):
    p1: Vec2
    p2: Vec2
    p3: Vec2
    p4: Vec2


class Polygon(BaseModel):
    points: PointList


class PointInPolygon(BaseModel):
    p: Vec2
    points: PointList
