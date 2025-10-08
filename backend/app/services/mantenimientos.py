# backend/app/services/mantenimientos.py
from typing import List, Union, Tuple
from sqlmodel import select, Session, func
from app.db.session import get_engine
from app.models.models import Mantenimiento as MantenimientoORM, Orden as OrdenORM, MtoTecnico as MtoTecnicoORM
from app.models.schemas import Mantenimiento, CrearMantenimiento, UpdateMantenimiento

engine = get_engine()

def get_next_mto_numero(session: Session) -> int:
    res = session.exec(select(func.max(MantenimientoORM.numero))).one()
    max_val = res or 0
    return max_val + 1

class MantenimientoService:
    @staticmethod
    def create_mantenimiento(payload: CrearMantenimiento) -> Union[Mantenimiento, None]:
        with Session(engine) as session:
            orden = session.get(OrdenORM, payload.consecutivo_orden)
            if not orden:
                return None
            numero = get_next_mto_numero(session)
            mto = MantenimientoORM(
                numero=numero,
                tipo=payload.tipo,
                descripcion=payload.descripcion,
                apertura=payload.apertura,
                precio=payload.precio,
                consecutivo_orden=payload.consecutivo_orden
            )
            session.add(mto)
            session.commit()
            session.refresh(mto)
            return Mantenimiento(**mto.dict())

    @staticmethod
    def get_all_mantenimientos() -> List[Mantenimiento]:
        with Session(engine) as session:
            rows = session.exec(select(MantenimientoORM)).all()
            return [Mantenimiento(**r.dict()) for r in rows]

    @staticmethod
    def update_mantenimiento(mto_numero: int, mto_data: UpdateMantenimiento) -> Union[Mantenimiento, int, bool, None, str]:
        with Session(engine) as session:
            mto = session.get(MantenimientoORM, mto_numero)
            if not mto:
                return None
            actualizar = mto_data.model_dump(exclude_unset=True)
            if not actualizar:
                return 304
            if 'cierre' in actualizar and actualizar['cierre'] is not None and mto.apertura >= actualizar['cierre']:
                return False
            if 'consecutivo_orden' in actualizar:
                nueva = session.get(OrdenORM, actualizar['consecutivo_orden'])
                if not nueva:
                    return f"Orden con CONSECUTIVO '{actualizar['consecutivo_orden']}' no fue encontrado"
                mto.consecutivo_orden = actualizar['consecutivo_orden']
            for k, v in actualizar.items():
                setattr(mto, k, v)
            session.add(mto)
            session.commit()
            session.refresh(mto)
            return Mantenimiento(**mto.dict())

    @staticmethod
    def delete_mantenimiento(mto_numero: int) -> Union[bool, None]:
        with Session(engine) as session:
            mto = session.get(MantenimientoORM, mto_numero)
            if not mto:
                return None
            # Si tiene técnicos asociados
            has_tec = session.exec(select(MtoTecnicoORM).where(MtoTecnicoORM.numero_mantenimiento == mto_numero)).first()
            if has_tec:
                return False
            session.delete(mto)
            session.commit()
            return True

    @staticmethod
    def search_and_sort_mantenimientos(q: str | None, order: str, offset: int, limit: int) -> Tuple[List[Mantenimiento], int]:
        with Session(engine) as session:
            stmt = select(MantenimientoORM)
            if q:
                stmt = stmt.where(MantenimientoORM.descripcion.contains(q))
            all_rows = session.exec(stmt).all()
            total = len(all_rows)
            rows = sorted(all_rows, key=lambda m: (m.descripcion or "").lower(), reverse=(order == "desc"))
            return [Mantenimiento(**r.dict()) for r in rows[offset: offset + limit]], total
