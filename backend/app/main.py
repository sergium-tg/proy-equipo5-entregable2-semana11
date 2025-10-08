import os
from datetime import datetime, timedelta
from typing import Optional

from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from jose import JWTError, jwt
from passlib.context import CryptContext

from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address
from slowapi.middleware import SlowAPIMiddleware

from app.services.bases import db_users

SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))

RATE_LIMIT_AUTH_PER_MIN = os.getenv("RATE_LIMIT_AUTH_PER_MIN", "5/minute")
RATE_LIMIT_API_PER_MIN = os.getenv("RATE_LIMIT_API_PER_MIN", "60/minute")
RATE_LIMIT_BURST = os.getenv("RATE_LIMIT_BURST", "10/second")

limiter = Limiter(key_func=get_remote_address, storage_uri="memory://")

try:
    from app.core.config import ALLOWED_ORIGINS
except ImportError:
    ALLOWED_ORIGINS = ["http://localhost:5173", "http://127.0.0.1:5173"]

from app.api.routers import clientes as clientes_router
from app.api.routers import ordenes as ordenes_router
from app.api.routers import mantenimientos as mantenimientos_router
from app.api.routers import tecnicos as tecnicos_router
from app.api.routers import mtoTecnicos as mtoTecnicos_router

from app.models.schemas import User, UserCreate, Token

app = FastAPI(title="API Taller_v2")

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("CORS_ORIGINS", "http://localhost:5173")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# Dependencia para obtener el usuario actual
async def get_current_user(request: Request, token: str = Depends(oauth2_scheme)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudo validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    if username not in db_users:
        raise credentials_exception
    request.state.user_id = username
    return User(username=username)

def user_or_ip_key(request: Request) -> str:
    return getattr(request.state, "user_id", None) or get_remote_address(request)

@app.get("/health")
async def health():
    """Endpoint público para verificar el estado de la API"""
    return {"status": "ok", "timestamp": datetime.utcnow().isoformat()}

@app.post("/auth/register", response_model=User, tags=["auth"])
@limiter.limit(RATE_LIMIT_API_PER_MIN)
async def register(request: Request, user: UserCreate):
    """Registrar un nuevo usuario"""
    if user.username in db_users:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El nombre de usuario ya está registrado"
        )
    db_users[user.username] = {"hashed_password": get_password_hash(user.password)}
    return User(username=user.username)

@app.post("/auth/login", response_model=Token, tags=["auth"])
@limiter.limit(RATE_LIMIT_AUTH_PER_MIN)
async def login(request: Request, form_data: OAuth2PasswordRequestForm = Depends()):
    """Iniciar sesión y obtener un token JWT"""
    record = db_users.get(form_data.username)
    if not record or not verify_password(form_data.password, record["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuario o contraseña incorrectos"
        )
    access_token = create_access_token({"sub": form_data.username})
    return Token(access_token=access_token)

@app.get("/me", response_model=User, tags=["auth"])
@limiter.limit(RATE_LIMIT_API_PER_MIN, key_func=user_or_ip_key)
async def me(request: Request, current_user: User = Depends(get_current_user)):
    return current_user

app.include_router(
    clientes_router.router,
    dependencies=[Depends(get_current_user)]
)
app.include_router(
    ordenes_router.router,
    dependencies=[Depends(get_current_user)]
)
app.include_router(
    mantenimientos_router.router,
    dependencies=[Depends(get_current_user)]
)
app.include_router(
    tecnicos_router.router,
    dependencies=[Depends(get_current_user)]
)
app.include_router(
    mtoTecnicos_router.router,
    dependencies=[Depends(get_current_user)]
)

from app.services import bases