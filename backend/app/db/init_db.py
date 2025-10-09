# backend/app/db/init_db.py
from sqlmodel import SQLModel, Session, select
from app.db.session import get_engine
from app.models.models import Cliente, Orden, Mantenimiento, Tecnico, MtoTecnico
from datetime import datetime

def init_db() -> None:
    """
    Crea las tablas (si no existen) e inserta datos de prueba mínima
    Si ya existen clientes, no vuelve a insertar (idempotente).
    """
    engine = get_engine()
    # crear tablas
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        # Si ya hay datos, no hacemos nada
        existing = session.exec(select(Cliente)).first()
        if existing:
            return

        # -- Clientes --
        cliente1 = Cliente(id=18008332, nombre="Juan", apellido="Duran", email="judu1@mail.com", contacto=3001000000, direccion="Av Caracas #123")
        cliente2 = Cliente(id=12350011, nombre="Diana", apellido="Valentina", email="diva1@mail.com", contacto=3002000000, direccion="Av Quito #772")
        cliente3 = Cliente(id=22315085, nombre="Adam", apellido="Santana", email="ansa1@mail.com", contacto=3003000000)

        session.add_all([cliente1, cliente2, cliente3])
        session.commit()  # commit para asegurar FK al insertar ordenes

        # -- Ordenes --
        orden1 = Orden(consecutivo=1, tipo="Mantenimiento", id_cliente=12350011)
        orden2 = Orden(consecutivo=2, tipo="Mantenimiento", id_cliente=12350011)
        orden3 = Orden(consecutivo=3, tipo="Mantenimiento", id_cliente=22315085)
        orden4 = Orden(consecutivo=4, tipo="Mantenimiento", id_cliente=18008332)

        session.add_all([orden1, orden2, orden3, orden4])
        session.commit()

        # -- Mantenimientos (usar objetos datetime para campos apertura/cierre) --
        mto1 = Mantenimiento(
            numero=1,
            tipo="Preventivo",
            apertura=datetime(2025, 7, 17, 8, 30),
            precio=150000,
            consecutivo_orden=1,
            descripcion="Cambio aceite"
        )
        mto2 = Mantenimiento(
            numero=2,
            tipo="Correctivo",
            apertura=datetime(2025, 8, 1, 10, 0),
            precio=1000000,
            consecutivo_orden=2,
            descripcion="Pintura"
        )
        mto3 = Mantenimiento(
            numero=3,
            tipo="Preventivo",
            apertura=datetime(2025, 8, 1, 14, 0),
            precio=500000,
            consecutivo_orden=3,
            descripcion="Alineacion"
        )
        mto4 = Mantenimiento(
            numero=4,
            tipo="Correctivo",
            apertura=datetime(2025, 8, 1, 10, 0),
            precio=100000,
            consecutivo_orden=3,
            descripcion="Cambio bujia"
        )
        mto5 = Mantenimiento(
            numero=5,
            tipo="Correctivo",
            apertura=datetime(2025, 8, 1, 10, 0),
            precio=100000,
            consecutivo_orden=4,
            descripcion="Reparacion Cableado"
        )

        session.add_all([mto1, mto2, mto3, mto4, mto5])
        session.commit()

        # -- Tecnicos --
        tecnico1 = Tecnico(id=123400, nombre="Andres", apellido="Molina", especialidad="Refrigeracion")
        tecnico2 = Tecnico(id=156300, nombre="Juan", apellido="Jaimes", especialidad="Electrico")
        tecnico3 = Tecnico(id=189011, nombre="Diana", apellido="Diaz", especialidad="Sensores")
        tecnico4 = Tecnico(id=200148, nombre="Eider", apellido="Molina", especialidad="Programacion")

        session.add_all([tecnico1, tecnico2, tecnico3, tecnico4])
        session.commit()

        # -- MtoTecnicos (relaciones) --
        mtoTec1 = MtoTecnico(numero_mantenimiento=1, id_tecnico=123400)
        mtoTec2 = MtoTecnico(numero_mantenimiento=2, id_tecnico=189011)
        mtoTec3 = MtoTecnico(numero_mantenimiento=2, id_tecnico=200148)
        mtoTec4 = MtoTecnico(numero_mantenimiento=4, id_tecnico=123400)
        mtoTec5 = MtoTecnico(numero_mantenimiento=5, id_tecnico=123400)
        mtoTec6 = MtoTecnico(numero_mantenimiento=3, id_tecnico=200148)

        session.add_all([mtoTec1, mtoTec2, mtoTec3, mtoTec4, mtoTec5, mtoTec6])
        session.commit()

        # listo
        print("init_db: tablas creadas y datos seed insertados.")
