from fastapi import APIRouter, HTTPException, Response, Query, status, Request
from typing import List
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.models.schemas import Cliente, CrearCliente, UpdateCliente
from app.services.clientes import ClienteService

router = APIRouter(prefix="", tags=["clientes"])
limiter = Limiter(key_func=get_remote_address, storage_uri="memory://")

def user_or_ip_key(request: Request) -> str:
    return getattr(request.state, "user_id", None) or get_remote_address(request)

# Crear instancia de CLIENTE
@router.post("/clientes", response_model=Cliente, status_code=status.HTTP_201_CREATED)
@limiter.limit("60/minute", key_func=user_or_ip_key)
def crear_cliente(request: Request, payload: CrearCliente) -> Cliente:
    cliente = ClienteService.create_cliente(payload)
    if cliente is None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, 
            detail="CLIENTE ya existe en la BD"
        )
    return cliente

# Listar todos los CLIENTES
@router.get("/clientes/todos", response_model=List[Cliente])
@limiter.limit("60/minute", key_func=user_or_ip_key)
def listar_clientes(request: Request) -> List[Cliente]:
    return ClienteService.get_all_clientes()

# Obtener CLIENTE por ID
@router.get("/clientes/{cliente_id}", response_model=Cliente)
@limiter.limit("60/minute", key_func=user_or_ip_key)
def info_cliente(request: Request, cliente_id: int) -> Cliente:
    cliente = ClienteService.get_cliente_by_id(cliente_id)
    if not cliente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Cliente con ID {cliente_id} no encontrado"
        )
    return cliente

# Actualizar información de CLIENTE
@router.put("/clientes/{cliente_id}", response_model=Cliente)
@limiter.limit("60/minute", key_func=user_or_ip_key)
def actualizar_cliente(request: Request, cliente_id: int, cliente_data: UpdateCliente) -> Cliente:
    updated_cliente = ClienteService.update_cliente(cliente_id, cliente_data)
    if updated_cliente is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Cliente no encontrado en la BD"
        )
    if updated_cliente == 304:
        return Response(status_code=status.HTTP_304_NOT_MODIFIED)
    return updated_cliente

# Eliminar CLIENTE por ID
@router.delete("/clientes/{cliente_id}", status_code=status.HTTP_204_NO_CONTENT)
@limiter.limit("60/minute", key_func=user_or_ip_key)
def eliminar_cliente(request: Request, cliente_id: int) -> Response:
    result = ClienteService.delete_cliente(cliente_id)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Cliente no encontrado en la BD"
        )
    if result is False:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No se puede eliminar el cliente porque tiene órdenes asociadas."
        )
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# Buscar y filtrar CLIENTES
@router.get("/clientes", response_model=List[Cliente])
@limiter.limit("60/minute", key_func=user_or_ip_key)
def busqueda_clientes(
    request: Request,
    response: Response,
    q: str | None = Query(None, description="Palabra clave a buscar"),
    sort: str = Query("apellido", regex="^(nombre|apellido)$", description="Ordenar por: nombre | apellido"),
    order: str = Query("asc", regex="^(asc|desc)$", description="Forma de ordenar: asc | desc"),
    offset: int = Query(0, ge=0, description="Inicio de los resultados"),
    limit: int = Query(10, ge=1, le=100, description="Número máximo de resultados a retornar"),
) -> List[Cliente]:
    results, total = ClienteService.search_and_sort_clientes(q, sort, order, offset, limit)
    response.headers["X-Total-Clientes"] = str(total)
    return results