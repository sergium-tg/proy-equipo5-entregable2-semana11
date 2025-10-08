from typing import List, Union, Tuple
from app.models.schemas import Mantenimiento, CrearMantenimiento, UpdateMantenimiento
from app.services.bases import db_ordenes, db_mantenimientos, db_mtoTecs, nuevo_numero

class MantenimientoService:
    @staticmethod
    def create_mantenimiento(payload: CrearMantenimiento) -> Union[Mantenimiento, None]:
        if payload.consecutivo_orden not in db_ordenes:
            return None
        mantenimiento = Mantenimiento(
            numero=nuevo_numero(),
            tipo=payload.tipo,
            descripcion=payload.descripcion,
            apertura=payload.apertura,
            precio=payload.precio,
            consecutivo_orden=payload.consecutivo_orden
        )
        db_mantenimientos[mantenimiento.numero] = mantenimiento
        orden_existente = db_ordenes[payload.consecutivo_orden]
        orden_existente.mantenimientos.append(mantenimiento)
        return mantenimiento

    @staticmethod
    def get_all_mantenimientos() -> List[Mantenimiento]:
        return list(db_mantenimientos.values())
        
    @staticmethod
    def update_mantenimiento(mto_numero: int, mto_data: UpdateMantenimiento) -> Union[Mantenimiento, int, bool, None]:
        mto = db_mantenimientos.get(mto_numero)
        if not mto:
            return None
        orden_anterior = mto.consecutivo_orden
        actualizar = mto_data.model_dump(exclude_unset=True)
        if not actualizar:
            return
        if 'cierre' in actualizar and actualizar['cierre'] is not None and mto.apertura >= actualizar['cierre']:
            return False
        if 'consecutivo_orden' in actualizar:
            consecutivo_orden_a_validar = actualizar['consecutivo_orden']
            if consecutivo_orden_a_validar != orden_anterior:
                orden_nueva = db_ordenes.get(consecutivo_orden_a_validar)
                if not orden_nueva:
                    return f"Orden con CONSECUTIVO '{consecutivo_orden_a_validar}' no fue encontrado" # Retorna str para 404
                orden_original = db_ordenes.get(orden_anterior)
                if orden_original:
                    orden_original.mantenimientos = [m for m in orden_original.mantenimientos if m.numero != mto_numero]
                mto.consecutivo_orden = consecutivo_orden_a_validar
                orden_nueva.mantenimientos.append(mto)
        for campo, valor in actualizar.items():
            setattr(mto, campo, valor)
            
        return mto

    @staticmethod
    def delete_mantenimiento(mto_numero: int) -> Union[bool, None]:
        mto = db_mantenimientos.get(mto_numero)
        if not mto:
            return None
        tiene_tecnicos = any(mto_num == mto_numero for (mto_num, _) in db_mtoTecs.keys())
        if tiene_tecnicos:
            return False
        orden = db_ordenes.get(mto.consecutivo_orden)
        if orden:
            orden.mantenimientos = [m for m in orden.mantenimientos if m.numero != mto_numero]            
        del db_mantenimientos[mto_numero]
        return True
    
    @staticmethod
    def search_and_sort_mantenimientos(q: str, order: str, offset: int, limit: int) -> Tuple[List[Mantenimiento], int]:
        results = list(db_mantenimientos.values())     
        if q:
            q_lower = q.lower()
            results = [
                m for m in results 
                if q_lower in m.descripcion.lower()
            ]
        es_reversa = (order == "desc") 
        results = sorted(
            results, 
            key=lambda m: m.descripcion.lower(),
            reverse=es_reversa
        )
        total = len(results)
        return results[offset: offset + limit], total