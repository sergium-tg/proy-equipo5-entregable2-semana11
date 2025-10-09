from sqlmodel import Session, select
from app.db.session import get_engine
from app.models.models import Cliente, Orden, Mantenimiento, Tecnico, MtoTecnico

engine = get_engine()
with Session(engine) as s:
    clientes = s.exec(select(Cliente)).all()
    ordenes = s.exec(select(Orden)).all()
    mantenimientos = s.exec(select(Mantenimiento)).all()
    tecnicos = s.exec(select(Tecnico)).all()
    mtos = s.exec(select(MtoTecnico)).all()
    print("clientes:", len(clientes))
    print("ordenes:", len(ordenes))
    print("mantenimientos:", len(mantenimientos))
    print("tecnicos:", len(tecnicos))
    print("mtos_tecnicos:", len(mtos))