"""Endpoints liés aux points."""
from fastapi import APIRouter, HTTPException
from geometry import points
# routers/points.py
from schemas import TwoPoints, PointCloud
router = APIRouter(prefix="/points", tags=["points"])


@router.post("/distance")
def points_distance(data: TwoPoints):
    return {"result": points.distance(data.p, data.q)}


@router.post("/midpoint")
def points_midpoint(data: TwoPoints):
    return {"result": points.midpoint(data.p, data.q)}


@router.post("/centroid")
def points_centroid(data: PointCloud):
    try:
        return {"result": points.centroid(data.points)}
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
