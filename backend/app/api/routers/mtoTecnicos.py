from fastapi import APIRouter, HTTPException, Response, status, Request
from typing import Dict, List
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.models.schemas import MtoTecnico, CrearMtoTecnico, UpdateMtoTecnico, Tecnico
from app.services.mtoTecnicos import MtoTecnicoService

router = APIRouter(prefix="", tags=["mtosTecs"])
limiter = Limiter(key_func=get_remote_address, storage_uri="memory://")

def user_or_ip_key(request: Request) -> str:
    return getattr(request.state, "user_id", None) or get_remote_address(request)

# Crear relación MANTENIMIENTO_TECNICO
@router.post("/mtosTecs", response_model=MtoTecnico, status_code=status.HTTP_201_CREATED)
@limiter.limit("60/minute", key_func=user_or_ip_key)
def crear_mto_tec(request: Request, payload: CrearMtoTecnico) -> MtoTecnico:
    result = MtoTecnicoService.create_mto_tec(payload)
    if result == 40401:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Mantenimiento no encontrado en BD"
        )
    if result == 40402:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Técnico no encontrado en BD"
        )
    if result == 409:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, 
            detail="Asignación MtoTec ya existe"
        )
    return result

# Listar todas las relaciones MANTENIMIENTO_TECNICO
@router.get("/mtosTecs/todos", response_model=List[Dict])
@limiter.limit("60/minute", key_func=user_or_ip_key)
def list_mantenimientos_tecnicos(request: Request) -> List[Dict]:
    return MtoTecnicoService.get_all_mto_tecs()

# Listar técnicos asignados a un mantenimiento
@router.get("/mtosTecs/mto/{numero_mto}", response_model=List[Tecnico])
@limiter.limit("60/minute", key_func=user_or_ip_key)
def listar_tecnicos_mantenimiento(request: Request, numero_mto: int) -> List[Tecnico]:
    result = MtoTecnicoService.get_tecnicos_by_mantenimiento(numero_mto)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Mantenimiento no encontrado"
        )
    if result == 40403:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="No se encontró técnico para ese mantenimiento"
        )
    return result

# Listar mantenimientos asignados a un técnico
@router.get("/mtosTecs/tecnico/{id_tecnico}", response_model=List[Dict])
@limiter.limit("60/minute", key_func=user_or_ip_key)
def listar_mantenimientos_tecnico(request: Request, id_tecnico: int) -> List[Dict]:
    result = MtoTecnicoService.get_mantenimientos_by_tecnico(id_tecnico)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Técnico no encontrado"
        )
    if result == 40404:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="No se encontró mantenimiento para ese técnico"
        )
    return result

# Actualizar relación MANTENIMIENTO_TECNICO
@router.put("/mtosTecs/{numero_mto}/{id_tecnico}", response_model=MtoTecnico)
@limiter.limit("60/minute", key_func=user_or_ip_key)
def actualizar_mto_tec(
    request: Request, 
    numero_mto: int, 
    id_tecnico: int, 
    payload: UpdateMtoTecnico
) -> MtoTecnico:
    result = MtoTecnicoService.update_mto_tec(numero_mto, id_tecnico, payload)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Asignación MtoTec no encontrada"
        )
    if result == 40401:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Mantenimiento nuevo no encontrado en BD"
        )
    if result == 40402:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Técnico nuevo no encontrado en BD"
        )
    if result == 409:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, 
            detail="La nueva Asignación MtoTec ya existe"
        )
    return result

# Eliminar relación MANTENIMIENTO_TECNICO
@router.delete("/mtosTecs/{numero_mto}/{id_tecnico}", status_code=status.HTTP_204_NO_CONTENT)
@limiter.limit("60/minute", key_func=user_or_ip_key)
def eliminar_mto_tec(request: Request, numero_mto: int, id_tecnico: int) -> Response:
    if not MtoTecnicoService.delete_mto_tec(numero_mto, id_tecnico):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Asignación MtoTec no encontrada"
        )
    return Response(status_code=status.HTTP_204_NO_CONTENT)