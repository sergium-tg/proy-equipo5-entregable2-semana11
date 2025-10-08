from fastapi import APIRouter, HTTPException, Response, Query, status
from typing import List
from app.models.schemas import Orden, CrearOrden, UpdateOrden
from app.services.ordenes import OrdenService

router = APIRouter(prefix="", tags=["ordenes"])

# creacion de instancia de la clase ORDEN
@router.post("/ordenes", response_model=Orden, status_code=status.HTTP_201_CREATED)
def crear_orden(payload: CrearOrden) -> Orden:
    orden = OrdenService.create_orden(payload)
    if orden is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Cliente con id {payload.id_cliente} no existe en la BD."
        )
    return orden

# encontrar ORDEN mediante su CONSECUTIVO
@router.get("/ordenes/{orden_consecutivo}", response_model=Orden)
def get_orden(orden_consecutivo: int) -> Orden:
    orden = OrdenService.get_orden_by_consecutivo(orden_consecutivo)
    if not orden:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ORDEN no encontrada, revise el CONSECUTIVO")
    return orden

# listar todas las ORDENES
@router.get("/ordenes/todos", response_model=List[Orden])
def list_ordenes() -> List[Orden]:
    return OrdenService.get_all_ordenes()

# Actualizar ORDEN mediante su CONSECUTIVO
@router.put("/ordenes/{orden_consecutivo}", response_model=Orden)
def actualizar_orden(orden_consecutivo: int, orden_data: UpdateOrden) -> Orden:
    updated_orden = OrdenService.update_orden(orden_consecutivo, orden_data)
    if updated_orden is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Orden no encontrada")
    if updated_orden is False:
        id_cliente_a_validar = orden_data.id_cliente
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"El Cliente con ID '{id_cliente_a_validar}' no fue encontrado")
    if updated_orden == 304:
        return Response(status_code=status.HTTP_304_NOT_MODIFIED)
    return updated_orden

# Eliminar ORDEN mediante su CONSECUTIVO
@router.delete("/ordenes/{orden_consecutivo}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_orden(orden_consecutivo: int) -> Response:
    result = OrdenService.delete_orden(orden_consecutivo)
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Orden no encontrada")
    if result is False:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="No se puede eliminar la orden porque tiene mantenimientos asociados."
        )
    return Response(status_code=status.HTTP_204_NO_CONTENT)