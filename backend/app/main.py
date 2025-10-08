from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from app.core.config import ALLOWED_ORIGINS
try:
    from app.core.config import ALLOWED_ORIGINS 
except ImportError:
    ALLOWED_ORIGINS = ["http://localhost:5173", "http://127.0.0.1:5173"]

from app.api.routers import clientes as clientes_router
from app.api.routers import ordenes as ordenes_router
from app.api.routers import mantenimientos as mantenimientos_router
from app.api.routers import tecnicos as tecnicos_router
from app.api.routers import mtoTecnicos as mtoTecnicos_router

app = FastAPI(title="API Taller")

# CORS (para que React pueda llamar a la API)
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rutas
app.include_router(clientes_router.router)
app.include_router(ordenes_router.router)
app.include_router(mantenimientos_router.router)
app.include_router(tecnicos_router.router)
app.include_router(mtoTecnicos_router.router)


#Se reemplaza la importación antigua in-memory por init_db ---
# from app.services import bases    # <-- Version antigua

from app.db.init_db import init_db

@app.on_event("startup")
def on_startup():
    init_db()
