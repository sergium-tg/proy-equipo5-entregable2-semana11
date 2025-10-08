from typing import List, Union, Tuple
from app.models.schemas import Tecnico, CrearTecnico, UpdateTecnico
from app.services.bases import db_tecnicos, db_mtoTecs

class TecnicoService:
    @staticmethod
    def create_tecnico(payload: CrearTecnico) -> Union[Tecnico, None]:
        if payload.id in db_tecnicos:
            return None        
        tecnico = Tecnico(**payload.model_dump())
        db_tecnicos[tecnico.id] = tecnico
        return tecnico

    @staticmethod
    def get_all_tecnicos() -> List[Tecnico]:
        return list(db_tecnicos.values())

    @staticmethod
    def get_tecnico_by_id(tecnico_id: int) -> Union[Tecnico, None]:
        return db_tecnicos.get(tecnico_id)

    @staticmethod
    def update_tecnico(tecnico_id: int, tecnico_data: UpdateTecnico) -> Union[Tecnico, int, None]:
        if tecnico_id not in db_tecnicos:
            return None
        tecnico_existente = db_tecnicos[tecnico_id]
        dato = tecnico_data.model_dump(exclude_unset=True) 
        if not dato:
            return 304
        updated_tecnico = tecnico_existente.model_copy(update=dato)
        db_tecnicos[tecnico_id] = updated_tecnico
        return updated_tecnico

    @staticmethod
    def delete_tecnico(tecnico_id: int) -> Union[bool, None]:
        if tecnico_id not in db_tecnicos:
            return None
        tiene_asignaciones = any(tec_id == tecnico_id for (_, tec_id) in db_mtoTecs.keys()) 
        if tiene_asignaciones:
            return False   
        del db_tecnicos[tecnico_id]
        return True

    @staticmethod
    def search_and_sort_tecnicos(q: str, sort: str, order: str, offset: int, limit: int) -> Tuple[List[Tecnico], int]:
        results = list(db_tecnicos.values())
        if q:
            q = q.lower()
            results = [
                t for t in results
                if q in t.nombre.lower() or q in t.apellido.lower()
            ]
        if sort:
            results = sorted(
                results,
                key=lambda t: getattr(t, sort).lower(),
                reverse=(order == "desc")
            )
        total = len(results)
        return results[offset: offset + limit], total