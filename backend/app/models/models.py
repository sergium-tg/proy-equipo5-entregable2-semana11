# backend/app/models/models.py
from __future__ import annotations
from typing import Optional
from sqlmodel import SQLModel, Field
from datetime import datetime

class Cliente(SQLModel, table=True):
    __tablename__ = "clientes"
    id: int = Field(primary_key=True)
    nombre: str
    apellido: str
    email: str
    contacto: int
    direccion: Optional[str] = None

class Orden(SQLModel, table=True):
    __tablename__ = "ordenes"
    consecutivo: int = Field(primary_key=True)
    tipo: str
    id_cliente: int = Field(foreign_key="clientes.id")

class Mantenimiento(SQLModel, table=True):
    __tablename__ = "mantenimientos"
    numero: int = Field(primary_key=True)
    tipo: str
    descripcion: Optional[str] = None
    apertura: datetime
    cierre: Optional[datetime] = None
    precio: float
    consecutivo_orden: int = Field(foreign_key="ordenes.consecutivo")

class Tecnico(SQLModel, table=True):
    __tablename__ = "tecnicos"
    id: int = Field(primary_key=True)
    nombre: str
    apellido: str
    especialidad: str

class MtoTecnico(SQLModel, table=True):
    __tablename__ = "mtos_tecnicos"
    numero_mantenimiento: int = Field(foreign_key="mantenimientos.numero", primary_key=True)
    id_tecnico: int = Field(foreign_key="tecnicos.id", primary_key=True)

