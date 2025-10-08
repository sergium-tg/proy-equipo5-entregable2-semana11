# backend/app/services/clientes.py
#Antes: los datos vivían solo en memoria (se perdían al reiniciar)y ahora: la DB (SQLite) guarda los datos en app.db, sobrevivientes a reinicios.

from typing import List, Tuple, Union
from sqlmodel import select
from app.models.schemas import Cliente as ClienteSchema, CrearCliente, UpdateCliente
from app.models.models import Cliente as ClienteModel, Orden as OrdenModel
from app.db.session import get_engine
from sqlmodel import Session

class ClienteService:
    @staticmethod
    def create_cliente(payload: CrearCliente) -> Union[dict, None]:
        engine = get_engine()
        with Session(engine) as session:
            # Verifica existencia por PK
            existing = session.get(ClienteModel, payload.id)
            if existing:
                return None
            # Crear instancia ORM
            cliente = ClienteModel(**payload.model_dump())
            session.add(cliente)
            session.commit()
            session.refresh(cliente)
            # devolver dict compatible con response_model (schemas.Cliente)
            return cliente.dict()

    @staticmethod
    def get_all_clientes() -> List[dict]:
        engine = get_engine()
        with Session(engine) as session:
            results = session.exec(select(ClienteModel)).all()
            # Convertir a lista de dicts (sin relaciones)
            return [r.dict() for r in results]

    @staticmethod
    def get_cliente_by_id(cliente_id: int) -> Union[dict, None]:
        engine = get_engine()
        with Session(engine) as session:
            cliente = session.get(ClienteModel, cliente_id)
            if not cliente:
                return None
            return cliente.dict()

    @staticmethod
    def update_cliente(cliente_id: int, cliente_data: UpdateCliente) -> Union[dict, int, None]:
        engine = get_engine()
        with Session(engine) as session:
            cliente = session.get(ClienteModel, cliente_id)
            if not cliente:
                return None
            actualizar = cliente_data.model_dump(exclude_unset=True, exclude={"id"})
            if not actualizar:
                return 304
            for k, v in actualizar.items():
                setattr(cliente, k, v)
            session.add(cliente)
            session.commit()
            session.refresh(cliente)
            return cliente.dict()

    @staticmethod
    def delete_cliente(cliente_id: int) -> Union[bool, None]:
        engine = get_engine()
        with Session(engine) as session:
            cliente = session.get(ClienteModel, cliente_id)
            if not cliente:
                return None
            # verificar si tiene órdenes asociadas
            ordenes = session.exec(select(OrdenModel).where(OrdenModel.id_cliente == cliente_id)).all()
            if ordenes:
                return False
            session.delete(cliente)
            session.commit()
            return True

    @staticmethod
    def search_and_sort_clientes(q: str, sort: str, order: str, offset: int, limit: int) -> Tuple[List[dict], int]:
        """
        Implementación simple: traemos todos y filtramos en Python.
        (fácil y fiable; si tu base crece cambiamos a filtros SQL).
        """
        engine = get_engine()
        with Session(engine) as session:
            results = session.exec(select(ClienteModel)).all()
            if q:
                q_lower = q.lower()
                results = [c for c in results if q_lower in c.nombre.lower() or q_lower in c.apellido.lower()]
            if sort:
                results = sorted(results, key=lambda c: getattr(c, sort).lower(), reverse=(order=="desc"))
            total = len(results)
            page = results[offset: offset + limit]
            return [c.dict() for c in page], total
