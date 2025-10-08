from typing import List, Union, Tuple
from app.models.schemas import Orden, CrearOrden, UpdateOrden
from app.services.bases import db_clientes, db_ordenes, nuevo_consecutivo

class OrdenService:
    @staticmethod
    def create_orden(payload: CrearOrden) -> Union[Orden, None]:
        if payload.id_cliente not in db_clientes:
            return None
        orden = Orden(
            consecutivo=nuevo_consecutivo(),
            tipo=payload.tipo,
            id_cliente=payload.id_cliente
        )
        db_ordenes[orden.consecutivo] = orden
        cliente_existente = db_clientes[payload.id_cliente]
        cliente_existente.ordenes.append(orden)
        return orden

    @staticmethod
    def get_orden_by_consecutivo(orden_consecutivo: int) -> Union[Orden, None]:
        return db_ordenes.get(orden_consecutivo)

    @staticmethod
    def get_all_ordenes() -> List[Orden]:
        return list(db_ordenes.values())

    @staticmethod
    def update_orden(orden_consecutivo: int, orden_data: UpdateOrden) -> Union[Orden, int, None]:
        orden = db_ordenes.get(orden_consecutivo)
        if not orden:
            return None 
        cliente_anterior = orden.id_cliente
        actualizar = orden_data.model_dump(exclude_unset=True)
        
        if not actualizar:
            return 304
        if 'id_cliente' in actualizar and actualizar['id_cliente'] != cliente_anterior:
            id_cliente_a_validar = actualizar['id_cliente']
            cliente_nuevo = db_clientes.get(id_cliente_a_validar)
            if not cliente_nuevo:
                return False
            cliente_original = db_clientes.get(cliente_anterior)
            if cliente_original:
                cliente_original.ordenes = [o for o in cliente_original.ordenes if o.consecutivo != orden_consecutivo]
            orden.id_cliente = id_cliente_a_validar
            cliente_nuevo.ordenes.append(orden)
        for campo, valor in actualizar.items():
            setattr(orden, campo, valor)
            
        return orden

    @staticmethod
    def delete_orden(orden_consecutivo: int) -> Union[bool, None]:
        orden = db_ordenes.get(orden_consecutivo)
        if not orden:
            return None        
        if orden.mantenimientos:
            return False
        id_cliente_asociado = orden.id_cliente
        cliente = db_clientes.get(id_cliente_asociado)
        if cliente:
            cliente.ordenes = [o for o in cliente.ordenes if o.consecutivo != orden_consecutivo]
        del db_ordenes[orden_consecutivo]
        return True