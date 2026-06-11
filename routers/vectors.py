"""Endpoints liés aux vecteurs."""
import math
from fastapi import APIRouter, HTTPException
from geometry import vectors
from schemas import (
    TwoVectors, OneVector, ScaleVector,
    LinearCombination, RotateVector, Lerp,
)

router = APIRouter(prefix="/vectors", tags=["vecteurs"])

# ... tous les @router.post(...) restent rigoureusement identiques.

@router.post("/add")
def vec_add(data: TwoVectors):
    return {"result": vectors.add(data.a, data.b)}


@router.post("/subtract")
def vec_subtract(data: TwoVectors):
    return {"result": vectors.subtract(data.a, data.b)}


@router.post("/scale")
def vec_scale(data: ScaleVector):
    return {"result": vectors.scale(data.v, data.k)}


@router.post("/linear-combination")
def vec_linear_combination(data: LinearCombination):
    return {"result": vectors.linear_combination(data.a, data.b, data.alpha, data.beta)}


@router.post("/dot")
def vec_dot(data: TwoVectors):
    return {"result": vectors.dot(data.a, data.b)}


@router.post("/cross")
def vec_cross(data: TwoVectors):
    return {"result": vectors.cross(data.a, data.b)}


@router.post("/norm")
def vec_norm(data: OneVector):
    return {"result": vectors.norm(data.v)}


@router.post("/perpendicular")
def vec_perpendicular(data: OneVector):
    return {"result": vectors.perpendicular(data.v)}


@router.post("/rotate")
def vec_rotate(data: RotateVector):
    return {"result": vectors.rotate(data.v, data.angle_rad)}


@router.post("/lerp")
def vec_lerp(data: Lerp):
    return {"result": vectors.lerp(data.a, data.b, data.t)}


@router.post("/heading")
def vec_heading(data: OneVector):
    rad = vectors.heading(data.v)
    return {"radians": rad, "degrees": math.degrees(rad)}


@router.post("/normalize")
def vec_normalize(data: OneVector):
    try:
        return {"result": vectors.normalize(data.v)}
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@router.post("/angle")
def vec_angle(data: TwoVectors):
    try:
        rad = vectors.angle_between(data.a, data.b)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    return {"radians": rad, "degrees": math.degrees(rad)}


@router.post("/project")
def vec_project(data: TwoVectors):
    try:
        return {"result": vectors.project(data.a, data.b)}
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
