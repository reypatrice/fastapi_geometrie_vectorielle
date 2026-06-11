"""Modèles de données (Pydantic) partagés par tous les routers.

Centraliser ici les schémas d'entrée évite de les redéfinir dans chaque router
et offre un seul endroit où lire le « contrat » de l'API. Les alias de type
(Vec2, Matrix3, PointList) nomment l'intention sans rien changer au comportement.
"""
from pydantic import BaseModel

Vec2 = list[float]                # un point ou un vecteur 2D : [x, y]
Matrix3 = list[list[float]]       # une matrice homogène 3x3
PointList = list[list[float]]     # une liste de points (figure, polygone...)


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
    matrices: list[Matrix3]


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