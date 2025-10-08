from typing import Dict
from datetime import datetime
from app.models.schemas import Cliente, Orden, Mantenimiento, Tecnico, MtoTecnico, User

# Simple in-memory store
db_users: Dict[str, User] = {} # nueva linea
db_clientes: Dict[int, Cliente] = {}
db_ordenes: Dict[int, Orden] = {}
db_mantenimientos: Dict[int, Mantenimiento] = {}
db_tecnicos: Dict[int, Tecnico] = {}
db_mtoTecs: Dict[tuple[int, int], MtoTecnico] = {}

_next_orden_consecutivo = 1
_next_mto_numero = 1

def nuevo_consecutivo() -> int:
    global _next_orden_consecutivo
    consecutivo = _next_orden_consecutivo
    _next_orden_consecutivo += 1
    while _next_orden_consecutivo in db_ordenes: # Por si alguien ya lo ha puesto manualmente o existe un hueco
        _next_orden_consecutivo += 1
    return consecutivo

def nuevo_numero() -> int:
    global _next_mto_numero
    numero = _next_mto_numero
    _next_mto_numero += 1
    while _next_mto_numero in db_mantenimientos:
        _next_mto_numero += 1
    return numero

## CASOS DE PRUEBA ##

# Casos CLIENTE

cliente1 = Cliente(id=18008332, nombre="Juan", apellido="Duran", email="judu1@mail.com", contacto=3001000000, direccion="Av Caracas #123")
cliente2 = Cliente(id=12350011, nombre="Diana", apellido=" Valentina", email="diva1@mail.com", contacto=3002000000, direccion="Av Quito #772")
cliente3 = Cliente(id=22315085, nombre="Adam", apellido="Santana", email="ansa1@mail.com", contacto=3003000000)
db_clientes[cliente1.id] = cliente1
db_clientes[cliente2.id] = cliente2
db_clientes[cliente3.id] = cliente3

# Casos ORDEN

orden1 = Orden(consecutivo=1, tipo="Mantenimiento", id_cliente=12350011)
orden2 = Orden(consecutivo=2, tipo="Mantenimiento", id_cliente=12350011)
orden3 = Orden(consecutivo=3, tipo="Mantenimiento", id_cliente=22315085)
orden4 = Orden(consecutivo=4, tipo="Mantenimiento", id_cliente=18008332)
db_ordenes[orden1.consecutivo] = orden1
db_ordenes[orden2.consecutivo] = orden2
db_ordenes[orden3.consecutivo] = orden3
db_ordenes[orden4.consecutivo] = orden4

# Casos MANTENIMIENTO

mto1 = Mantenimiento(numero=1, tipo="Preventivo", apertura=datetime(2025, 7, 17, 8, 30), precio=150000, consecutivo_orden=1, descripcion="Cambio aceite")
mto2 = Mantenimiento(numero=2, tipo="Correctivo", apertura=datetime(2025, 8, 1, 10, 0), precio=1000000, consecutivo_orden=2, descripcion="Pintura")
mto3 = Mantenimiento(numero=3, tipo="Preventivo", apertura=datetime(2025, 8, 1, 14, 0), precio=500000, consecutivo_orden=3, descripcion="Alineacion")
mto4 = Mantenimiento(numero=4, tipo="Correctivo", apertura=datetime(2025, 8, 1, 10, 0), precio=100000, consecutivo_orden=3, descripcion="Cambio bujia")
mto5 = Mantenimiento(numero=5, tipo="Correctivo", apertura=datetime(2025, 8, 1, 10, 0), precio=100000, consecutivo_orden=4, descripcion="Reparacion Cableado")
db_mantenimientos[mto1.numero] = mto1
db_mantenimientos[mto2.numero] = mto2
db_mantenimientos[mto3.numero] = mto3
db_mantenimientos[mto4.numero] = mto4
db_mantenimientos[mto5.numero] = mto5

# Casos TECNICO

tecnico1 = Tecnico(id=123400, nombre="Andres", apellido="Molina", especialidad="Refrigeracion")
tecnico2 = Tecnico(id=156300, nombre="Juan", apellido="Jaimes", especialidad="Electrico")
tecnico3 = Tecnico(id=189011, nombre="Diana", apellido="Diaz", especialidad="Sensores")
tecnico4 = Tecnico(id=200148, nombre="Eider", apellido="Molina", especialidad="Programacion")
db_tecnicos[tecnico1.id] = tecnico1
db_tecnicos[tecnico2.id] = tecnico2
db_tecnicos[tecnico3.id] = tecnico3
db_tecnicos[tecnico4.id] = tecnico4


# Relaciones ORDEN_MANTENIMIENTO

orden1.mantenimientos.append(mto1)
orden2.mantenimientos.append(mto2)
orden3.mantenimientos.append(mto3)
orden3.mantenimientos.append(mto4)
orden4.mantenimientos.append(mto5)

# Relaciones CLIENTE_ORDEN

cliente2.ordenes.append(orden1)
cliente2.ordenes.append(orden2)
cliente3.ordenes.append(orden3)
cliente1.ordenes.append(orden4)

# Relaciones MANTENIMIENTOS_TECNICO

mtoTec1 = MtoTecnico(numero_mantenimiento=1, id_tecnico=123400)
db_mtoTecs[(1, 123400)] = mtoTec1

mtoTec2 = MtoTecnico(numero_mantenimiento=2, id_tecnico=189011)
db_mtoTecs[(2, 189011)] = mtoTec2

mtoTec3 = MtoTecnico(numero_mantenimiento=2, id_tecnico=200148)
db_mtoTecs[(2, 200148)] = mtoTec3

mtoTec4 = MtoTecnico(numero_mantenimiento=4, id_tecnico=123400)
db_mtoTecs[(4, 123400)] = mtoTec4

mtoTec5 = MtoTecnico(numero_mantenimiento=5, id_tecnico=123400)
db_mtoTecs[(5, 123400)] = mtoTec5

mtoTec6 = MtoTecnico(numero_mantenimiento=3, id_tecnico=200148)
db_mtoTecs[(3, 200148)] = mtoTec6