from typing import List, Optional
from datetime import datetime
from sqlmodel import SQLModel
from app.producto.model import ProductoBase


class ProductoCreate(ProductoBase):
    categoria_ids: List[int] = []
    ingrediente_ids: List[int] = []


class CategoriaInProducto(SQLModel):
    id: int
    nombre: str


class IngredienteInProducto(SQLModel):
    id: int
    nombre: str
    es_alergeno: bool


class ProductoRead(ProductoBase):
    id: int
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None
    categorias: List[CategoriaInProducto] = []
    ingredientes: List[IngredienteInProducto] = []


class ProductoUpdate(ProductoBase):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    precio_base: Optional[float] = None
    imagenes_url: Optional[List[str]] = None
    stock_cantidad: Optional[int] = None
    disponible: Optional[bool] = None
    categoria_ids: Optional[List[int]] = None
    ingrediente_ids: Optional[List[int]] = None
