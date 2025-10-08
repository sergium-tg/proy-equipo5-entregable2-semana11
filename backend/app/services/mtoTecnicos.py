from typing import List, Dict, Union, Tuple
from app.models.schemas import MtoTecnico, CrearMtoTecnico, UpdateMtoTecnico, Tecnico
from app.services.bases import db_mantenimientos, db_tecnicos, db_mtoTecs

class MtoTecnicoService:
    @staticmethod
    def create_mto_tec(payload: CrearMtoTecnico) -> Union[MtoTecnico, int, None]:
        if payload.numero_mantenimiento not in db_mantenimientos:
            return 40401
        if payload.id_tecnico not in db_tecnicos:
            return 40402
        clave = (payload.numero_mantenimiento, payload.id_tecnico)
        if clave in db_mtoTecs:
            return 409
        db_mtoTecs[clave] = MtoTecnico(**payload.model_dump())
        return db_mtoTecs[clave]

    @staticmethod
    def get_all_mto_tecs() -> List[Dict]:
        relations_list = []
        for (mto_num, tec_id), _ in db_mtoTecs.items():
            mantenimiento = db_mantenimientos.get(mto_num)
            tecnico = db_tecnicos.get(tec_id)
            if mantenimiento and tecnico:
                relations_list.append({
                    "mantenimiento": mantenimiento,
                    "tecnico": tecnico
                })
        return relations_list

    @staticmethod
    def get_tecnicos_by_mantenimiento(numero_mto: int) -> Union[List[Tecnico], None, int]:
        if numero_mto not in db_mantenimientos:
            return None
        tecnicos_asignados: List[Tecnico] = []
        encontrado_en_asignacion = False
        for (mto_num, tec_id), _ in db_mtoTecs.items():
            if mto_num == numero_mto:
                encontrado_en_asignacion = True
                tecnico = db_tecnicos.get(tec_id)
                if tecnico:
                    tecnicos_asignados.append(tecnico)          
        if not encontrado_en_asignacion and not tecnicos_asignados:
            return 40403
        return tecnicos_asignados

    @staticmethod
    def update_mto_tec(numero_mto: int, id_tecnico: int, payload: UpdateMtoTecnico) -> Union[MtoTecnico, int, None]:
        clave_actual = (numero_mto, id_tecnico)
        clave_nueva = (payload.numero_mantenimiento, payload.id_tecnico)
        if clave_actual not in db_mtoTecs:
            return None
        if payload.numero_mantenimiento not in db_mantenimientos:
            return 40401
        if payload.id_tecnico not in db_tecnicos:
            return 40402
        if clave_actual != clave_nueva:
            if clave_nueva in db_mtoTecs:
                return 409
            del db_mtoTecs[clave_actual]
        db_mtoTecs[clave_nueva] = MtoTecnico(**payload.model_dump())
        return db_mtoTecs[clave_nueva]

    @staticmethod
    def delete_mto_tec(numero_mto: int, id_tecnico: int) -> bool:
        clave = (numero_mto, id_tecnico)
        if clave not in db_mtoTecs:
            return False
        del db_mtoTecs[clave]
        return True