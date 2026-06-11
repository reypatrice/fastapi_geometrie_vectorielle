"""Endpoints liés aux droites, segments et polygones."""
from fastapi import APIRouter, HTTPException
from geometry import shapes
# routers/shapes.py
from schemas import (
    ThreePoints, PointAndSegment, TwoSegments, Polygon, PointInPolygon,
)
router = APIRouter(prefix="/shapes", tags=["formes"])

@router.post("/orientation")
def shape_orientation(data: ThreePoints):
    return {"result": shapes.orientation(data.a, data.b, data.c)}


@router.post("/collinear")
def shape_collinear(data: ThreePoints):
    return {"result": shapes.collinear(data.a, data.b, data.c)}


@router.post("/point-line-distance")
def shape_point_line_distance(data: PointAndSegment):
    try:
        return {"result": shapes.point_line_distance(data.p, data.a, data.b)}
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@router.post("/point-segment-distance")
def shape_point_segment_distance(data: PointAndSegment):
    return {"result": shapes.point_segment_distance(data.p, data.a, data.b)}


@router.post("/segment-intersection")
def shape_segment_intersection(data: TwoSegments):
    return {"point": shapes.segment_intersection(data.p1, data.p2, data.p3, data.p4)}


@router.post("/polygon/area")
def shape_polygon_area(data: Polygon):
    try:
        return {"result": shapes.polygon_area(data.points)}
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@router.post("/polygon/perimeter")
def shape_polygon_perimeter(data: Polygon):
    return {"result": shapes.polygon_perimeter(data.points)}


@router.post("/polygon/centroid")
def shape_polygon_centroid(data: Polygon):
    return {"result": shapes.polygon_centroid(data.points)}


@router.post("/polygon/contains")
def shape_point_in_polygon(data: PointInPolygon):
    return {"result": shapes.point_in_polygon(data.p, data.points)}


@router.post("/polygon/is-convex")
def shape_is_convex(data: Polygon):
    try:
        return {"result": shapes.is_convex(data.points)}
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))