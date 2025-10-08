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
                    # Se usa .model_dump() para convertir la instancia de Pydantic a un dict
                    "mantenimiento": mantenimiento.model_dump(), 
                    "tecnico": tecnico.model_dump()             
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
    
    def get_mantenimientos_by_tecnico(id_tecnico: int) -> Union[List[Dict], None, int]:
        # Suponiendo que tienes un diccionario db_tecnicos y db_mantenimientos
        from app.services.bases import db_mantenimientos, db_tecnicos, db_mtoTecs 

        if id_tecnico not in db_tecnicos:
            return None  # Técnico no encontrado
        
        mantenimientos_asignados: List[Dict] = []
        encontrado_en_asignacion = False
        
        # db_mtoTecs es un diccionario con clave (numero_mto, id_tecnico)
        for (mto_num, tec_id), mto_tec_obj in db_mtoTecs.items():
            if tec_id == id_tecnico:
                encontrado_en_asignacion = True
                mantenimiento = db_mantenimientos.get(mto_num)
                if mantenimiento:
                    # Devuelve el Mantenimiento y la relación MtoTec, o solo el Mantenimiento
                    # Si el router espera List[Dict], devolvemos el diccionario completo de la relación
                    mantenimientos_asignados.append({
                        "mantenimiento": mantenimiento,
                        "asignacion": mto_tec_obj.model_dump() # La data extra de la relación
                    })

        if not encontrado_en_asignacion and not mantenimientos_asignados:
            return 40404 # Nuevo código de error para "no se encontró mantenimiento para ese técnico"
            
        return mantenimientos_asignados

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