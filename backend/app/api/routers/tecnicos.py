from fastapi import APIRouter, HTTPException, Response, Query, status, Request
from typing import List
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.models.schemas import Tecnico, CrearTecnico, UpdateTecnico
from app.services.tecnicos import TecnicoService

router = APIRouter(prefix="", tags=["tecnicos"])
limiter = Limiter(key_func=get_remote_address, storage_uri="memory://")

def user_or_ip_key(request: Request) -> str:
    return getattr(request.state, "user_id", None) or get_remote_address(request)

# Crear instancia de TECNICO
@router.post("/tecnicos", response_model=Tecnico, status_code=status.HTTP_201_CREATED)
@limiter.limit("60/minute", key_func=user_or_ip_key)
def crear_tecnico(request: Request, payload: CrearTecnico) -> Tecnico:
    tecnico = TecnicoService.create_tecnico(payload)
    if tecnico is None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, 
            detail="TECNICO ya existe en la BD"
        )
    return tecnico

# Listar todos los TECNICOS
@router.get("/tecnicos/todos", response_model=List[Tecnico])
@limiter.limit("60/minute", key_func=user_or_ip_key)
def listar_tecnicos(request: Request) -> List[Tecnico]:
    return TecnicoService.get_all_tecnicos()

# Obtener TECNICO por ID
@router.get("/tecnicos/{id_tecnico}", response_model=Tecnico)
@limiter.limit("60/minute", key_func=user_or_ip_key)
def info_tecnico(request: Request, id_tecnico: int) -> Tecnico:
    tecnico = TecnicoService.get_tecnico_by_id(id_tecnico)
    if not tecnico:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="TECNICO no encontrado, revise el ID"
        )
    return tecnico

# Actualizar TECNICO por ID
@router.put("/tecnicos/{id_tecnico}", response_model=Tecnico)
@limiter.limit("60/minute", key_func=user_or_ip_key)
def actualizar_tecnico(request: Request, id_tecnico: int, tecnico_data: UpdateTecnico) -> Tecnico:
    updated_tecnico = TecnicoService.update_tecnico(id_tecnico, tecnico_data)
    if updated_tecnico is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Técnico con ID {id_tecnico} no encontrado"
        )
    if updated_tecnico == 304:
        return Response(status_code=status.HTTP_304_NOT_MODIFIED)
    return updated_tecnico

# Eliminar TECNICO por ID
@router.delete("/tecnicos/{id_tecnico}", status_code=status.HTTP_204_NO_CONTENT)
@limiter.limit("60/minute", key_func=user_or_ip_key)
def eliminar_tecnico(request: Request, id_tecnico: int) -> Response:
    result = TecnicoService.delete_tecnico(id_tecnico)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="TECNICO no encontrado en la BD"
        )
    if result is False:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No se puede eliminar el TECNICO porque tiene Mantenimientos asignados (MtoTecnicos)."
        )
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# Buscar y filtrar TECNICOS
@router.get("/tecnicos", response_model=List[Tecnico])
@limiter.limit("60/minute", key_func=user_or_ip_key)
def busqueda_tecnicos(
    request: Request,
    response: Response,
    q: str | None = Query(None, description="Palabra clave a buscar por nombre o apellido"),
    sort: str = Query("apellido", regex="^(nombre|apellido)$", description="Ordenar por: nombre | apellido"),
    order: str = Query("asc", regex="^(asc|desc)$", description="Forma de ordenar: asc | desc"),
    offset: int = Query(0, ge=0, description="Inicio de los resultados"),
    limit: int = Query(10, ge=1, le=100, description="Número máximo de resultados a retornar"),
) -> List[Tecnico]:
    results, total = TecnicoService.search_and_sort_tecnicos(q, sort, order, offset, limit)
    response.headers["X-Total-Tecnicos"] = str(total)
    return results