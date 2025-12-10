"""
Esquemas Pydantic para validación de datos
"""
from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

# Esquemas para Usuario
class UsuarioBase(BaseModel):
    nombre: str
    email: EmailStr

class UsuarioCreate(UsuarioBase):
    pass

class UsuarioUpdate(BaseModel):
    nombre: Optional[str] = None
    email: Optional[EmailStr] = None
    activo: Optional[bool] = None

class UsuarioResponse(UsuarioBase):
    id: int
    activo: bool
    fecha_creacion: datetime
    fecha_actualizacion: datetime
    
    class Config:
        from_attributes = True

# Esquemas para Producto
class ProductoBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    precio: int
    stock: int = 0

class ProductoCreate(ProductoBase):
    pass

class ProductoUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    precio: Optional[int] = None
    stock: Optional[int] = None

class ProductoResponse(ProductoBase):
    id: int
    fecha_creacion: datetime
    fecha_actualizacion: datetime
    
    class Config:
        from_attributes = True
