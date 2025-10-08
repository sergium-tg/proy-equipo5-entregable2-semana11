from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# Asumiendo que app.core.config existe
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

# Importación de servicios para inicializar datos en memoria
from app.services import bases
# La inicialización de los datos de prueba ocurre al importar bases.py
# y bases._initialize_consecutives() se ejecuta al final.