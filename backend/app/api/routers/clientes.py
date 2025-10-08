from fastapi import APIRouter, HTTPException, Response, Query, status
from typing import List
from app.models.schemas import Cliente, CrearCliente, UpdateCliente
from app.services.clientes import ClienteService

router = APIRouter(prefix="", tags=["clientes"])

# creacion de instacia de la clase CLIENTE
@router.post("/clientes", response_model=Cliente, status_code=status.HTTP_201_CREATED)
def crear_cliente(payload: CrearCliente) -> Cliente:
    cliente = ClienteService.create_cliente(payload)
    if cliente is None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="CLIENTE ya existe en la BD")
    return cliente
    
# listar todos los CLIENTES
@router.get("/clientes/todos", response_model=List[Cliente])
def list_clientes_all() -> List[Cliente]:
    return ClienteService.get_all_clientes()

# listar Cliente
@router.get("/clientes/{cliente_id}", response_model=Cliente)
def get_cliente(cliente_id: int) -> Cliente:
    cliente = ClienteService.get_cliente_by_id(cliente_id)
    if not cliente:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Cliente con ID {cliente_id} no encontrado")
    return cliente

# actualizar info Cliente
@router.put("/clientes/{cliente_id}", response_model=Cliente)
def actualizar_cliente(cliente_id: int, cliente_data: UpdateCliente) -> Cliente:
    updated_cliente = ClienteService.update_cliente(cliente_id, cliente_data)
    if updated_cliente is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cliente no encontrado en la BD")
    if updated_cliente == 304:
        return Response(status_code=status.HTTP_304_NOT_MODIFIED)
    return updated_cliente

# Eliminar Cliente por id
@router.delete("/clientes/{cliente_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_cliente(cliente_id: int) -> Response:
    result = ClienteService.delete_cliente(cliente_id)
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cliente no encontrado en la BD")
    if result is False:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No se puede eliminar el cliente porque tiene órdenes asociadas."
        )
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# Buscar CLIENTE mediante atributo NOMBRE o APELLIDO y ordenar
@router.get("/clientes", response_model=List[Cliente])
def list_clientes(
    response: Response,
    q: str | None = Query(None, description="Palabra clave a buscar"),
    sort: str = Query("apellido", regex="^(nombre|apellido)$", description="Ordenar por: nombre | apellido"),
    order: str = Query("asc", regex="^(asc|desc)$", description="Forma de ordenar: asc | desc"),
    offset: int = Query(0, ge=0, description="Índice de inicio de los resultados"),
    limit: int = Query(10, ge=1, le=100, description="Número máximo de resultados a retornar"),
) -> List[Cliente]:
    results, total = ClienteService.search_and_sort_clientes(q, sort, order, offset, limit)
    response.headers["X-Total-Clientes"] = str(total)
    return results