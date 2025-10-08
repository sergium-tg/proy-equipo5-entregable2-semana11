from fastapi import APIRouter, HTTPException, Response, Query, status
from typing import List
from app.models.schemas import Mantenimiento, CrearMantenimiento, UpdateMantenimiento
from app.services.mantenimientos import MantenimientoService

router = APIRouter(prefix="", tags=["mantenimientos"])

# creacion de instancia de la clase MANTENIMIENTO
@router.post("/mantenimientos", response_model=Mantenimiento, status_code=status.HTTP_201_CREATED)
def crear_mantenimiento(payload: CrearMantenimiento) -> Mantenimiento:
    mantenimiento = MantenimientoService.create_mantenimiento(payload)
    if mantenimiento is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Orden con consecutivo {payload.consecutivo_orden} no existe en la BD."
        )
    return mantenimiento

# Actualizar MANTENIMIENTO mediante su NUMERO
@router.put("/mantenimientos/{mto_numero}", response_model=Mantenimiento)
def actualizar_mto(mto_numero: int, mto_data: UpdateMantenimiento) -> Mantenimiento:
    updated_mto = MantenimientoService.update_mantenimiento(mto_numero, mto_data)
    if updated_mto is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Mantenimiento no encontrado")
    if updated_mto == 304:
        return Response(status_code=status.HTTP_304_NOT_MODIFIED)
    if updated_mto is False:
        mto = MantenimientoService.get_all_mantenimientos()
        mto_existente = next((m for m in mto if m.numero == mto_numero), None)
        cierre = mto_data.cierre.isoformat() if mto_data.cierre else 'None'
        apertura = mto_existente.apertura.isoformat() if mto_existente else 'N/A'
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=f"La fecha de cierre ({cierre}) debe ser posterior a la fecha de apertura ({apertura})."
        )
    if isinstance(updated_mto, str):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"La {updated_mto}")
    return updated_mto

# listar todos los MANTENIMIENTOS
@router.get("/mantenimientos/todos", response_model=List[Mantenimiento])
def list_mantenimientos_all() -> List[Mantenimiento]:
    return MantenimientoService.get_all_mantenimientos()

# Eliminar instancia de MANTENIMIENTO
@router.delete("/mantenimientos/{mto_numero}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_mantenimiento(mto_numero: int) -> Response:
    result = MantenimientoService.delete_mantenimiento(mto_numero)
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Mantenimiento no encontrado")
    if result is False:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No se puede eliminar el Mantenimiento porque tiene Técnicos asociados."
        )
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# Buscar MATENIMIENTO mediante atributo DESCRIPCION y ordenar
@router.get("/mantenimientos", response_model=List[Mantenimiento])
def list_mantenimientos(
    response: Response,
    q: str | None = Query(None, description="Palabra clave a buscar en la descripción del mantenimiento"),
    order: str = Query("asc", regex="^(asc|desc)$", description="Forma de ordenar: asc | desc"),
    offset: int = Query(0, ge=0, description="Índice de inicio de los resultados"),
    limit: int = Query(10, ge=1, le=100, description="Número máximo de resultados a retornar"),
) -> List[Mantenimiento]:
    results, total = MantenimientoService.search_and_sort_mantenimientos(q, order, offset, limit)
    response.headers["X-Total-Mantenimientos"] = str(total)
    return results