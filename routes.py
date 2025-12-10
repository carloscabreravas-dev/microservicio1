"""
Rutas de la API
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from database import get_db, Usuario, Producto
from schemas import (
    UsuarioCreate, UsuarioResponse, UsuarioUpdate,
    ProductoCreate, ProductoResponse, ProductoUpdate
)

router = APIRouter()

# ==================== RUTAS DE USUARIOS ====================

@router.get("/usuarios", response_model=List[UsuarioResponse])
async def obtener_usuarios(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Obtener lista de usuarios
    
    - **skip**: número de registros a saltar (paginación)
    - **limit**: número máximo de registros a devolver
    """
    usuarios = db.query(Usuario).offset(skip).limit(limit).all()
    return usuarios

@router.get("/usuarios/{usuario_id}", response_model=UsuarioResponse)
async def obtener_usuario(usuario_id: int, db: Session = Depends(get_db)):
    """Obtener un usuario por ID"""
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Usuario con ID {usuario_id} no encontrado"
        )
    return usuario

@router.post("/usuarios", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED)
async def crear_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    """Crear un nuevo usuario"""
    # Verificar si el email ya existe
    db_usuario = db.query(Usuario).filter(Usuario.email == usuario.email).first()
    if db_usuario:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El email ya está registrado"
        )
    
    nuevo_usuario = Usuario(**usuario.model_dump())
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    return nuevo_usuario

@router.put("/usuarios/{usuario_id}", response_model=UsuarioResponse)
async def actualizar_usuario(usuario_id: int, usuario: UsuarioUpdate, db: Session = Depends(get_db)):
    """Actualizar un usuario"""
    db_usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not db_usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Usuario con ID {usuario_id} no encontrado"
        )
    
    datos_actualizacion = usuario.model_dump(exclude_unset=True)
    for campo, valor in datos_actualizacion.items():
        setattr(db_usuario, campo, valor)
    
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario

@router.delete("/usuarios/{usuario_id}")
async def eliminar_usuario(usuario_id: int, db: Session = Depends(get_db)):
    """Eliminar un usuario"""
    db_usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not db_usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Usuario con ID {usuario_id} no encontrado"
        )
    
    db.delete(db_usuario)
    db.commit()
    return {"mensaje": "Usuario eliminado correctamente"}

# ==================== RUTAS DE PRODUCTOS ====================

@router.get("/productos", response_model=List[ProductoResponse])
async def obtener_productos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Obtener lista de productos
    
    - **skip**: número de registros a saltar (paginación)
    - **limit**: número máximo de registros a devolver
    """
    productos = db.query(Producto).offset(skip).limit(limit).all()
    return productos

@router.get("/productos/{producto_id}", response_model=ProductoResponse)
async def obtener_producto(producto_id: int, db: Session = Depends(get_db)):
    """Obtener un producto por ID"""
    producto = db.query(Producto).filter(Producto.id == producto_id).first()
    if not producto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Producto con ID {producto_id} no encontrado"
        )
    return producto

@router.post("/productos", response_model=ProductoResponse, status_code=status.HTTP_201_CREATED)
async def crear_producto(producto: ProductoCreate, db: Session = Depends(get_db)):
    """Crear un nuevo producto"""
    nuevo_producto = Producto(**producto.model_dump())
    db.add(nuevo_producto)
    db.commit()
    db.refresh(nuevo_producto)
    return nuevo_producto

@router.put("/productos/{producto_id}", response_model=ProductoResponse)
async def actualizar_producto(producto_id: int, producto: ProductoUpdate, db: Session = Depends(get_db)):
    """Actualizar un producto"""
    db_producto = db.query(Producto).filter(Producto.id == producto_id).first()
    if not db_producto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Producto con ID {producto_id} no encontrado"
        )
    
    datos_actualizacion = producto.model_dump(exclude_unset=True)
    for campo, valor in datos_actualizacion.items():
        setattr(db_producto, campo, valor)
    
    db.add(db_producto)
    db.commit()
    db.refresh(db_producto)
    return db_producto

@router.delete("/productos/{producto_id}")
async def eliminar_producto(producto_id: int, db: Session = Depends(get_db)):
    """Eliminar un producto"""
    db_producto = db.query(Producto).filter(Producto.id == producto_id).first()
    if not db_producto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Producto con ID {producto_id} no encontrado"
        )
    
    db.delete(db_producto)
    db.commit()
    return {"mensaje": "Producto eliminado correctamente"}
