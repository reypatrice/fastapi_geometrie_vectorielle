import os

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from slowapi.util import get_remote_address

from routers import vectors, points, matrices, shapes

app = FastAPI(title="API de géométrie vectorielle 2D")

# --- Limitation de débit (rate limiting) ---------------------------------
# Protège l'API publique contre les abus : au-delà de la limite, un client
# (identifié par son adresse IP) reçoit un code 429 "Too Many Requests".
# La limite se règle via la variable d'environnement RATE_LIMIT.
rate_limit = os.environ.get("RATE_LIMIT", "100/minute")
limiter = Limiter(key_func=get_remote_address, default_limits=[rate_limit])
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)

# --- CORS ----------------------------------------------------------------
# Autorise l'appel de l'API depuis un navigateur ou un front-end. En public,
# lister les domaines réellement autorisés dans ALLOWED_ORIGINS (séparés par
# des virgules) plutôt que de laisser "*" qui ouvre à tout le monde.
allowed_origins = os.environ.get("ALLOWED_ORIGINS", "*").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Routes --------------------------------------------------------------
app.include_router(vectors.router)
app.include_router(points.router)
app.include_router(matrices.router)
app.include_router(shapes.router)


@app.get("/")
def root():
    return {"message": "API de géométrie vectorielle 2D", "docs": "/docs"}


if __name__ == "__main__":
    # En local   : `python main.py`  ->  http://127.0.0.1:8000
    # Sur Render : Start Command      ->  uvicorn main:app --host 0.0.0.0 --port $PORT
    #              (la plateforme fournit PORT et expose l'app sur onrender.com)
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False)
