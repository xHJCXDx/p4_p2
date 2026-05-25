from typing import List, Optional
from datetime import datetime
from sqlmodel import Field, Relationship, SQLModel
from app.producto.model import ProductoIngredienteLink

class IngredienteBase(SQLModel):
    nombre: str = Field(index=True, unique=True)
    descripcion: Optional[str] = None
    es_alergeno: bool = Field(default=False)

class Ingrediente(IngredienteBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    productos: List["Producto"] = Relationship(back_populates="ingredientes", link_model=ProductoIngredienteLink)
