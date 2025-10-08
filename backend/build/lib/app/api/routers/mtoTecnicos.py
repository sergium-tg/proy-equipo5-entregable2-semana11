from fastapi import APIRouter, HTTPException, Response, status
from typing import Dict, List, Union
from app.models.schemas import MtoTecnico, CrearMtoTecnico, UpdateMtoTecnico, Tecnico
from app.services.mtoTecnicos import MtoTecnicoService

router = APIRouter(prefix="", tags=["mtosTecs"])

# creacion relacion MANTENIMIENTO_TECNICO
@router.post("/mtosTecs", response_model=MtoTecnico, status_code=status.HTTP_201_CREATED)
def crear_mto_tec(payload: CrearMtoTecnico) -> MtoTecnico:
    result = MtoTecnicoService.create_mto_tec(payload)
    if result == 40401:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Mantenimiento no encontrado en BD")
    if result == 40402:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Técnico no encontrado en BD")
    if result == 409:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Asignación MtoTec ya existe") 
    return result

# listar todas las relaciones MANTENIMIENTO_TECNICO
@router.get("/mtosTecs/todos", response_model=List[Dict])
def list_mantenimientos_tecnicos() -> List[Dict]:
    return MtoTecnicoService.get_all_mto_tecs()

# listar todas las relaciones MANTENIMIENTO_TECNICO por numero_mto
@router.get("/mtosTecs/{numero_mto}", response_model=List[Tecnico])
def get_tecnicos_mantenimiento(numero_mto: int) -> List[Tecnico]:
    result = MtoTecnicoService.get_tecnicos_by_mantenimiento(numero_mto)
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Mantenimiento no encontrado")
    if result == 40403:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="no se encontró tecnico para ese mantenimiento"
        )
    return result

# Actualizar relacion MANTENIMIENTO_TECNICO por numero_mto + id_tecnico
@router.put("/mtosTecs/{numero_mto}/{id_tecnico}", response_model=MtoTecnico)
def actualizar_mto_tec(numero_mto: int, id_tecnico: int, payload: UpdateMtoTecnico) -> MtoTecnico:
    result = MtoTecnicoService.update_mto_tec(numero_mto, id_tecnico, payload)
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Asignación MtoTec no encontrada")
    if result == 40401:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Mantenimiento nuevo no encontrado en BD")
    if result == 40402:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Técnico nuevo no encontrado en BD")
    if result == 409:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="La nueva Asignación MtoTec ya existe")
    return result

# Eliminar relación MANTENIMIENTO_TECNICO por numero_mto + id_tecnico
@router.delete("/mtosTecs/{numero_mto}/{id_tecnico}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_mto_tec(numero_mto: int, id_tecnico: int) -> Response:
    if not MtoTecnicoService.delete_mto_tec(numero_mto, id_tecnico):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Asignación MtoTec no encontrada")
    return Response(status_code=status.HTTP_204_NO_CONTENT)