# backend/app/services/clientes.py
from typing import List, Tuple, Union
from sqlmodel import select, Session
from app.db.session import get_engine
from app.models.models import Cliente as ClienteORM, Orden as OrdenORM
from app.models.schemas import Cliente, CrearCliente, UpdateCliente

engine = get_engine()

class ClienteService:
    @staticmethod
    def create_cliente(payload: CrearCliente) -> Cliente | None:
        with Session(engine) as session:
            existing = session.get(ClienteORM, payload.id)
            if existing:
                return None
            cliente = ClienteORM(**payload.model_dump())
            session.add(cliente)
            session.commit()
            session.refresh(cliente)
            return Cliente(**cliente.dict())

    @staticmethod
    def get_all_clientes() -> List[Cliente]:
        with Session(engine) as session:
            rows = session.exec(select(ClienteORM)).all()
            return [Cliente(**r.dict()) for r in rows]

    @staticmethod
    def get_cliente_by_id(cliente_id: int) -> Union[Cliente, None]:
        with Session(engine) as session:
            c = session.get(ClienteORM, cliente_id)
            if not c:
                return None
            # cargar ordenes relacionadas
            # usaremos la representación de schemas: construir Ordens desde ORM
            c_dict = c.dict()
            # No incluimos `ordenes` como objetos ORM complejos; pydantic espera lista de Orden dicts
            c_dict["ordenes"] = [o.dict() for o in c.ordenes] if c.ordenes else []
            return Cliente(**c_dict)

    @staticmethod
    def update_cliente(cliente_id: int, payload: UpdateCliente) -> Union[Cliente, int, None]:
        with Session(engine) as session:
            c = session.get(ClienteORM, cliente_id)
            if not c:
                return None
            update_data = payload.model_dump(exclude_unset=True)
            if not update_data:
                return 304
            for k, v in update_data.items():
                setattr(c, k, v)
            session.add(c)
            session.commit()
            session.refresh(c)
            c_dict = c.dict()
            c_dict["ordenes"] = [o.dict() for o in c.ordenes] if c.ordenes else []
            return Cliente(**c_dict)

    @staticmethod
    def delete_cliente(cliente_id: int) -> Union[bool, None]:
        with Session(engine) as session:
            c = session.get(ClienteORM, cliente_id)
            if not c:
                return None
            if c.ordenes:
                return False
            session.delete(c)
            session.commit()
            return True

    @staticmethod
    def search_and_sort_clientes(q: str | None, sort: str, order: str, offset: int, limit: int) -> Tuple[List[Cliente], int]:
        with Session(engine) as session:
            stmt = select(ClienteORM)
            if q:
                stmt = stmt.where((ClienteORM.nombre.contains(q)) | (ClienteORM.apellido.contains(q)))
            order_col = getattr(ClienteORM, sort)
            stmt = stmt.order_by(order_col.asc() if order == "asc" else order_col.desc())
            all_rows = session.exec(stmt).all()
            total = len(all_rows)
            rows = all_rows[offset: offset + limit]
            return [Cliente(**{**r.dict(), "ordenes": [o.dict() for o in r.ordenes]}) for r in rows], total
