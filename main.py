from fastapi import FastAPI
from routers import vectors, points, matrices, shapes

app = FastAPI(title="API de géométrie vectorielle 2D")
app.include_router(vectors.router)
app.include_router(points.router)
app.include_router(matrices.router)
app.include_router(shapes.router)
@app.get("/")
def root():
    return {"message": "API de géométrie vectorielle 2D", "docs": "/docs"}
