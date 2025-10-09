# backend/app/services/mtoTecnicos.py
from typing import List, Dict, Union
from sqlmodel import select, Session
from app.db.session import get_engine
from app.models.models import MtoTecnico as MtoTecnicoORM, Mantenimiento as MantenimientoORM, Tecnico as TecnicoORM
from app.models.schemas import MtoTecnico, CrearMtoTecnico, UpdateMtoTecnico, Tecnico

engine = get_engine()

class MtoTecnicoService:
    @staticmethod
    def create_mto_tec(payload: CrearMtoTecnico) -> Union[MtoTecnico, int]:
        with Session(engine) as session:
            mto = session.get(MantenimientoORM, payload.numero_mantenimiento)
            if not mto:
                return 40401
            tec = session.get(TecnicoORM, payload.id_tecnico)
            if not tec:
                return 40402
            clave = (payload.numero_mantenimiento, payload.id_tecnico)
            exists = session.get(MtoTecnicoORM, clave)
            if exists:
                return 409
            assoc = MtoTecnicoORM(**payload.model_dump())
            session.add(assoc)
            session.commit()
            session.refresh(assoc)
            return MtoTecnico(**assoc.dict())

    @staticmethod
    def get_all_mto_tecs() -> List[Dict]:
        with Session(engine) as session:
            rows = session.exec(select(MtoTecnicoORM)).all()
            result = []
            for r in rows:
                mto = session.get(MantenimientoORM, r.numero_mantenimiento)
                tec = session.get(TecnicoORM, r.id_tecnico)
                result.append({"mantenimiento": mto.dict() if mto else None, "tecnico": tec.dict() if tec else None})
            return result

    @staticmethod
    def get_tecnicos_by_mantenimiento(numero_mto: int) -> Union[List[Tecnico], int, None]:
        with Session(engine) as session:
            mto = session.get(MantenimientoORM, numero_mto)
            if not mto:
                return None
            rows = session.exec(select(MtoTecnicoORM).where(MtoTecnicoORM.numero_mantenimiento == numero_mto)).all()
            if not rows:
                return 40403
            tecnicos = []
            for r in rows:
                tec = session.get(TecnicoORM, r.id_tecnico)
                if tec:
                    tecnicos.append(Tecnico(**tec.dict()))
            return tecnicos

    @staticmethod
    def get_mantenimientos_by_tecnico(id_tecnico: int) -> Union[List[Dict], int, None]:
        with Session(engine) as session:
            tec = session.get(TecnicoORM, id_tecnico)
            if not tec:
                return None
            rows = session.exec(select(MtoTecnicoORM).where(MtoTecnicoORM.id_tecnico == id_tecnico)).all()
            if not rows:
                return 40404
            result = []
            for r in rows:
                mto = session.get(MantenimientoORM, r.numero_mantenimiento)
                if mto:
                    result.append(mto.dict())
            return result

    @staticmethod
    def update_mto_tec(numero_mto: int, id_tecnico: int, payload: UpdateMtoTecnico) -> Union[MtoTecnico, int, None]:
        with Session(engine) as session:
            clave = (numero_mto, id_tecnico)
            obj = session.get(MtoTecnicoORM, clave)
            if not obj:
                return None
            # validar nuevos ids
            if not session.get(MantenimientoORM, payload.numero_mantenimiento):
                return 40401
            if not session.get(TecnicoORM, payload.id_tecnico):
                return 40402
            nueva_clave = (payload.numero_mantenimiento, payload.id_tecnico)
            if nueva_clave != clave:
                exists = session.get(MtoTecnicoORM, nueva_clave)
                if exists:
                    return 409
                # eliminar actual y crear nuevo (pk compuesta)
                session.delete(obj)
                session.commit()
                nuevo = MtoTecnicoORM(**payload.model_dump())
                session.add(nuevo)
                session.commit()
                session.refresh(nuevo)
                return MtoTecnico(**nuevo.dict())
            # si no cambia la clave, solo asegurar valores (aunque pk = same)
            return MtoTecnico(**obj.dict())

    @staticmethod
    def delete_mto_tec(numero_mto: int, id_tecnico: int) -> bool:
        with Session(engine) as session:
            clave = (numero_mto, id_tecnico)
            obj = session.get(MtoTecnicoORM, clave)
            if not obj:
                return False
            session.delete(obj)
            session.commit()
            return True
