# backend/app/services/tecnicos.py
from typing import List, Union, Tuple
from sqlmodel import select, Session
from app.db.session import get_engine
from app.models.models import Tecnico as TecnicoORM, MtoTecnico as MtoTecnicoORM
from app.models.schemas import Tecnico, CrearTecnico, UpdateTecnico

engine = get_engine()

class TecnicoService:
    @staticmethod
    def create_tecnico(payload: CrearTecnico) -> Union[Tecnico, None]:
        with Session(engine) as session:
            existing = session.get(TecnicoORM, payload.id)
            if existing:
                return None
            t = TecnicoORM(**payload.model_dump())
            session.add(t)
            session.commit()
            session.refresh(t)
            return Tecnico(**t.dict())

    @staticmethod
    def get_all_tecnicos() -> List[Tecnico]:
        with Session(engine) as session:
            rows = session.exec(select(TecnicoORM)).all()
            return [Tecnico(**r.dict()) for r in rows]

    @staticmethod
    def get_tecnico_by_id(tecnico_id: int) -> Union[Tecnico, None]:
        with Session(engine) as session:
            t = session.get(TecnicoORM, tecnico_id)
            if not t:
                return None
            return Tecnico(**t.dict())

    @staticmethod
    def update_tecnico(tecnico_id: int, tecnico_data: UpdateTecnico) -> Union[Tecnico, int, None]:
        with Session(engine) as session:
            t = session.get(TecnicoORM, tecnico_id)
            if not t:
                return None
            update = tecnico_data.model_dump(exclude_unset=True)
            if not update:
                return 304
            for k, v in update.items():
                setattr(t, k, v)
            session.add(t)
            session.commit()
            session.refresh(t)
            return Tecnico(**t.dict())

    @staticmethod
    def delete_tecnico(tecnico_id: int) -> Union[bool, None]:
        with Session(engine) as session:
            t = session.get(TecnicoORM, tecnico_id)
            if not t:
                return None
            has_assign = session.exec(select(MtoTecnicoORM).where(MtoTecnicoORM.id_tecnico == tecnico_id)).first()
            if has_assign:
                return False
            session.delete(t)
            session.commit()
            return True

    @staticmethod
    def search_and_sort_tecnicos(q: str | None, sort: str, order: str, offset: int, limit: int) -> Tuple[List[Tecnico], int]:
        with Session(engine) as session:
            stmt = select(TecnicoORM)
            if q:
                stmt = stmt.where((TecnicoORM.nombre.contains(q)) | (TecnicoORM.apellido.contains(q)))
            rows = session.exec(stmt).all()
            rows_sorted = sorted(rows, key=lambda t: getattr(t, sort).lower(), reverse=(order == "desc"))
            total = len(rows_sorted)
            return [Tecnico(**r.dict()) for r in rows_sorted[offset: offset + limit]], total