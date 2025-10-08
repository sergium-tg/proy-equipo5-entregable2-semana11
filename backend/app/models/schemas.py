from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Literal, List, Optional

###### Modelos de Autenticación ######

class User(BaseModel):
    username: str

class UserCreate(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


###### Entidad Tecnico ######

class Tecnico(BaseModel):
    id: int
    nombre: str
    apellido: str
    especialidad: str

class CrearTecnico(Tecnico):
    pass

class UpdateTecnico(BaseModel):
    nombre: str | None = None
    apellido: str | None = None
    especialidad: str | None = None


###### Entidad MANTENIMIENTO ######

class Mantenimiento(BaseModel):
    numero: int
    tipo: str
    descripcion: str | None = None
    apertura: datetime
    cierre: datetime | None = None
    precio: float
    consecutivo_orden: int

class CrearMantenimiento(BaseModel):
    tipo: Literal["Correctivo", "Preventivo"]
    descripcion: str | None = None
    apertura: datetime
    precio: float
    consecutivo_orden: int

class UpdateMantenimiento(BaseModel):
    consecutivo_orden: int | None = None 
    tipo: Literal["Correctivo", "Preventivo"] | None = None
    descripcion: str | None = None
    cierre: datetime | None = None
    precio: float | None = None
    

###### Entidad ORDEN ######

class Orden(BaseModel):
    consecutivo: int
    tipo: str
    id_cliente: int 
    mantenimientos: List[Mantenimiento] = []

class CrearOrden(BaseModel):
    consecutivo: int | None = None
    tipo: Literal["Mantenimiento", "Venta", "Mixto"]
    id_cliente: int

class UpdateOrden(BaseModel):
    id_cliente: int | None = None


###### Entidad CLIENTE ######

class Cliente(BaseModel):
    id: int
    nombre: str
    apellido: str
    email: EmailStr
    contacto: int
    direccion: str | None = None
    ordenes: List[Orden] = []

class CrearCliente(BaseModel):
    id: int = Field(..., ge=100000, description="El documento debe tener al menos 6 digitos")
    nombre: str = Field(..., min_length=1, description="Digitar el NOMBRE del cliente")
    apellido: str = Field(..., min_length=1, description="Digitar el APELLIDO del cliente")
    email: EmailStr = Field(description="Agregar correo electronico")
    contacto: int = Field(..., ge=300000000, description="Numero telefonico requerido")
    direccion: str | None = None

class UpdateCliente(BaseModel):
    nombre: str | None = None
    apellido: str | None = None
    email: EmailStr | None = None
    contacto: int | None = None
    direccion: str | None = None


###### Entidad MANTENIMIENTO_TECNICO ######

class MtoTecnico(BaseModel):
    numero_mantenimiento: int
    id_tecnico: int

class CrearMtoTecnico(MtoTecnico):
    pass

class UpdateMtoTecnico(MtoTecnico):
    pass