import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_add_endpoint():
    response = client.post("/vectors/add", json={"a": [1, 2], "b": [3, 4]})
    assert response.status_code == 200
    assert response.json()["result"] == [4.0, 6.0]


def test_angle_endpoint_returns_degrees():
    response = client.post("/vectors/angle", json={"a": [1, 0], "b": [0, 1]})
    assert response.status_code == 200
    assert response.json()["degrees"] == 90.0


def test_normalize_zero_returns_400():
    # Le cas d'erreur métier devient un code 400, pas un plantage 500.
    response = client.post("/vectors/normalize", json={"v": [0, 0]})
    assert response.status_code == 400


def test_invalid_input_returns_422():
    # Donnée mal formée : la validation Pydantic répond 422 automatiquement.
    response = client.post("/vectors/norm", json={"v": "pas un vecteur"})
    assert response.status_code == 422

def test_distance_endpoint():
    response = client.post("/points/distance", json={"p": [0, 0], "q": [3, 4]})
    assert response.status_code == 200
    assert response.json()["result"] == 5.0

def test_centroid_endpoint():
    response = client.post("/points/centroid", json={"points": [[0, 0], [3, 0], [0, 3]]})
    assert response.json()["result"] == [1.0, 1.0]

def test_centroid_empty_returns_400():
    response = client.post("/points/centroid", json={"points": []})
    assert response.status_code == 400

def test_transform_rotate_endpoint():
    response = client.post("/transform/rotate", json={"points": [[1, 0]], "angle_deg": 90})
    x, y = response.json()["points"][0]
    assert x == pytest.approx(0.0, abs=1e-9)
    assert y == pytest.approx(1.0, abs=1e-9)


def test_matrices_multiply_then_apply():
    t1 = client.post("/matrices/translation", json={"dx": 1, "dy": 2}).json()["matrix"]
    t2 = client.post("/matrices/translation", json={"dx": 3, "dy": 4}).json()["matrix"]
    composed = client.post("/matrices/multiply", json={"matrices": [t1, t2]}).json()["matrix"]
    response = client.post("/matrices/apply", json={"points": [[0, 0]], "matrix": composed})
    assert response.json()["points"][0] == pytest.approx([4.0, 6.0])


def test_matrices_invert_singular_returns_400():
    singular = [[1, 1, 0], [1, 1, 0], [0, 0, 1]]
    response = client.post("/matrices/invert", json={"matrix": singular})
    assert response.status_code == 400

def test_polygon_area_endpoint():
    response = client.post("/shapes/polygon/area",
                           json={"points": [[0, 0], [1, 0], [1, 1], [0, 1]]})
    assert response.json()["result"] == 1.0

def test_polygon_contains_endpoint():
    square = [[0, 0], [4, 0], [4, 4], [0, 4]]
    inside = client.post("/shapes/polygon/contains", json={"p": [2, 2], "points": square})
    outside = client.post("/shapes/polygon/contains", json={"p": [5, 5], "points": square})
    assert inside.json()["result"] is True
    assert outside.json()["result"] is False

def test_segment_intersection_none_endpoint():
    response = client.post("/shapes/segment-intersection",
                           json={"p1": [0, 0], "p2": [1, 0], "p3": [0, 1], "p4": [1, 1]})
    assert response.json()["point"] is None