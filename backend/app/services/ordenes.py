# backend/app/services/ordenes.py
from typing import List, Union
from sqlmodel import select, Session, func
from app.db.session import get_engine
from app.models.models import Orden as OrdenORM, Cliente as ClienteORM, Mantenimiento as MantenimientoORM
from app.models.schemas import Orden, CrearOrden, UpdateOrden

engine = get_engine()

def get_next_consecutivo(session: Session) -> int:
    res = session.exec(select(func.max(OrdenORM.consecutivo))).one()
    max_val = res or 0
    return max_val + 1

class OrdenService:
    @staticmethod
    def create_orden(payload: CrearOrden) -> Union[Orden, None]:
        with Session(engine) as session:
            cliente = session.get(ClienteORM, payload.id_cliente)
            if not cliente:
                return None
            consecutivo = payload.consecutivo if payload.consecutivo else get_next_consecutivo(session)
            orden = OrdenORM(consecutivo=consecutivo, tipo=payload.tipo, id_cliente=payload.id_cliente)
            session.add(orden)
            session.commit()
            session.refresh(orden)
            # commit ya asocia, construir schema
            orden_dict = orden.dict()
            orden_dict["mantenimientos"] = [m.dict() for m in orden.mantenimientos] if orden.mantenimientos else []
            return Orden(**orden_dict)

    @staticmethod
    def get_orden_by_consecutivo(orden_consecutivo: int) -> Union[Orden, None]:
        with Session(engine) as session:
            o = session.get(OrdenORM, orden_consecutivo)
            if not o:
                return None
            o_dict = o.dict()
            o_dict["mantenimientos"] = [m.dict() for m in o.mantenimientos] if o.mantenimientos else []
            return Orden(**o_dict)

    @staticmethod
    def get_all_ordenes() -> List[Orden]:
        with Session(engine) as session:
            rows = session.exec(select(OrdenORM)).all()
            result = []
            for r in rows:
                d = r.dict()
                d["mantenimientos"] = [m.dict() for m in r.mantenimientos] if r.mantenimientos else []
                result.append(Orden(**d))
            return result

    @staticmethod
    def update_orden(orden_consecutivo: int, orden_data: UpdateOrden) -> Union[Orden, int, None, bool]:
        with Session(engine) as session:
            o = session.get(OrdenORM, orden_consecutivo)
            if not o:
                return None
            update = orden_data.model_dump(exclude_unset=True)
            if not update:
                return 304
            if "id_cliente" in update and update["id_cliente"] != o.id_cliente:
                cliente_nuevo = session.get(ClienteORM, update["id_cliente"])
                if not cliente_nuevo:
                    return False
                o.id_cliente = update["id_cliente"]
            for k, v in update.items():
                setattr(o, k, v)
            session.add(o)
            session.commit()
            session.refresh(o)
            o_dict = o.dict()
            o_dict["mantenimientos"] = [m.dict() for m in o.mantenimientos] if o.mantenimientos else []
            return Orden(**o_dict)

    @staticmethod
    def delete_orden(orden_consecutivo: int) -> Union[bool, None]:
        with Session(engine) as session:
            o = session.get(OrdenORM, orden_consecutivo)
            if not o:
                return None
            if o.mantenimientos:
                return False
            # eliminar referencia en cliente no es necesario: relación se maneja por FK
            session.delete(o)
            session.commit()
            return True
