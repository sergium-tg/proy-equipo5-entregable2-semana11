from typing import List, Dict, Any, Union, Tuple
from app.models.schemas import Cliente, CrearCliente, UpdateCliente
from app.services.bases import db_clientes, db_ordenes

class ClienteService:
    @staticmethod
    def create_cliente(payload: CrearCliente) -> Cliente:
        if payload.id in db_clientes:
            return None
        cliente = Cliente(**payload.model_dump())
        db_clientes[cliente.id] = cliente
        return cliente

    @staticmethod
    def get_all_clientes() -> List[Cliente]:
        return list(db_clientes.values())

    @staticmethod
    def get_cliente_by_id(cliente_id: int) -> Union[Cliente, None]:
        return db_clientes.get(cliente_id)

    @staticmethod
    def update_cliente(cliente_id: int, cliente_data: UpdateCliente) -> Union[Cliente, int, None]:
        if cliente_id not in db_clientes:
            return None
        cliente_existente = db_clientes[cliente_id]
        actualizar_data = cliente_data.model_dump(exclude_unset=True, exclude={'id', 'ordenes'})
        if not actualizar_data:
            return 304
        updated_cliente = cliente_existente.model_copy(update=actualizar_data)
        updated_cliente.ordenes = cliente_existente.ordenes 
        db_clientes[cliente_id] = updated_cliente
        return updated_cliente

    @staticmethod
    def delete_cliente(cliente_id: int) -> bool:
        if cliente_id not in db_clientes:
            return None
        cliente = db_clientes[cliente_id]
        if cliente.ordenes:
            return False
        del db_clientes[cliente_id]
        return True

    @staticmethod
    def search_and_sort_clientes(q: str, sort: str, order: str, offset: int, limit: int) -> Tuple[List[Cliente], int]:
        results = list(db_clientes.values())
        if q:
            q = q.lower()
            results = [
                c for c in results 
                if q in c.nombre.lower() or q in c.apellido.lower()
            ]
        if sort:
            results = sorted(
                results, 
                key=lambda c: getattr(c, sort).lower(),
                reverse=(order == "desc")
            )
        total = len(results)
        return results[offset: offset + limit], total