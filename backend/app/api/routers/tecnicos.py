from fastapi import APIRouter, HTTPException, Response, Query, status
from typing import List
from app.models.schemas import Tecnico, CrearTecnico, UpdateTecnico
from app.services.tecnicos import TecnicoService

router = APIRouter(prefix="", tags=["tecnicos"])

# creacion de instacia de la clase TECNICO
@router.post("/tecnicos", response_model=Tecnico, status_code=status.HTTP_201_CREATED)
def crear_tecnico(payload: CrearTecnico) -> Tecnico:
    tecnico = TecnicoService.create_tecnico(payload)
    if tecnico is None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="TECNICO ya existe en la BD")
    return tecnico
    
# listar todos los TECNICOS
@router.get("/tecnicos/todos", response_model=List[Tecnico])
def list_tecnicos_all() -> List[Tecnico]:
    return TecnicoService.get_all_tecnicos()

# encontrar TECNICO mediante su ID
@router.get("/tecnicos/{id_tecnico}", response_model=Tecnico)
def get_tecnico(id_tecnico: int) -> Tecnico:
    tecnico = TecnicoService.get_tecnico_by_id(id_tecnico)
    if not tecnico:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="TECNICO no encontrado, revise el ID")
    return tecnico

# Actualizar TECNICO mediante su ID
@router.put("/tecnicos/{id_tecnico}", response_model=Tecnico)
def actualizar_tecnico(id_tecnico: int, tecnico_data: UpdateTecnico) -> Tecnico:
    updated_tecnico = TecnicoService.update_tecnico(id_tecnico, tecnico_data)
    
    if updated_tecnico is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Técnico con ID {id_tecnico} no encontrado")
    if updated_tecnico == 304:
        return Response(status_code=status.HTTP_304_NOT_MODIFIED)
        
    return updated_tecnico

# Eliminar TECNICO mediante su ID
@router.delete("/tecnicos/{id_tecnico}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_tecnico(id_tecnico: int) -> Response:
    result = TecnicoService.delete_tecnico(id_tecnico)
    
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="TECNICO no encontrado en la BD")
    if result is False:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No se puede eliminar el TECNICO porque tiene Mantenimientos asignados (MtoTecnicos)."
        )
        
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# Buscar TECNICO mediante atributo NOMBRE o APELLIDO y ordenar
@router.get("/tecnicos", response_model=List[Tecnico])
def list_tecnicos(
    response: Response,
    q: str | None = Query(None, description="Palabra clave a buscar por nombre o apellido"),
    sort: str = Query("apellido", regex="^(nombre|apellido)$", description="Ordenar por: nombre | apellido"),
    order: str = Query("asc", regex="^(asc|desc)$", description="Forma de ordenar: asc | desc"),
    offset: int = Query(0, ge=0, description="Índice de inicio de los resultados"),
    limit: int = Query(10, ge=1, le=100, description="Número máximo de resultados a retornar"),
) -> List[Tecnico]:
    results, total = TecnicoService.search_and_sort_tecnicos(q, sort, order, offset, limit)
    response.headers["X-Total-Tecnicos"] = str(total)
    return results