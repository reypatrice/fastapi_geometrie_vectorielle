"""Endpoints liés aux matrices de transformation.
Deux niveaux :
- bas niveau (/matrices/*) : fabriquer une matrice, la composer, l'inverser,
  l'appliquer ;
- haut niveau (/transform/*) : transformer directement une figure.
"""
from fastapi import APIRouter, HTTPException
from geometry import matrices
# routers/matrices.py
from schemas import (
    RotationParams, ScalingParams, TranslationParams,
    ShearParams, ReflectionParams, MatrixList, OneMatrix, ApplyMatrix,
    RotateFigure, ScaleFigure, TranslateFigure,
)

router = APIRouter(tags=["matrices"])

# --- Endpoints : construction de matrices ---------------------------------

@router.get("/matrices/identity")
def matrix_identity():
    return {"matrix": matrices.identity()}


@router.post("/matrices/rotation")
def matrix_rotation(data: RotationParams):
    return {"matrix": matrices.rotation(data.angle_deg, center=data.center)}


@router.post("/matrices/scaling")
def matrix_scaling(data: ScalingParams):
    return {"matrix": matrices.scaling(data.sx, data.sy, center=data.center)}


@router.post("/matrices/translation")
def matrix_translation(data: TranslationParams):
    return {"matrix": matrices.translation(data.dx, data.dy)}


@router.post("/matrices/shear")
def matrix_shear(data: ShearParams):
    return {"matrix": matrices.shear(data.kx, data.ky)}


@router.post("/matrices/reflection")
def matrix_reflection(data: ReflectionParams):
    return {"matrix": matrices.reflection(data.angle_deg)}


@router.post("/matrices/multiply")
def matrix_multiply(data: MatrixList):
    return {"matrix": matrices.multiply(data.matrices)}


@router.post("/matrices/invert")
def matrix_invert(data: OneMatrix):
    try:
        return {"matrix": matrices.invert(data.matrix)}
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@router.post("/matrices/apply")
def matrix_apply(data: ApplyMatrix):
    try:
        return {"points": matrices.apply(data.points, data.matrix)}
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))


# --- Endpoints : transformation directe d'une figure (haut niveau) --------

@router.post("/transform/rotate", tags=["transformations"])
def transform_rotate(data: RotateFigure):
    matrix = matrices.rotation(data.angle_deg, center=data.center)
    return {"points": matrices.apply(data.points, matrix)}


@router.post("/transform/scale", tags=["transformations"])
def transform_scale(data: ScaleFigure):
    matrix = matrices.scaling(data.sx, data.sy, center=data.center)
    return {"points": matrices.apply(data.points, matrix)}


@router.post("/transform/translate", tags=["transformations"])
def transform_translate(data: TranslateFigure):
    matrix = matrices.translation(data.dx, data.dy)
    return {"points": matrices.apply(data.points, matrix)}