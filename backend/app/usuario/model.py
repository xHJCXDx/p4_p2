"""Modelos de Usuario, Rol y UsuarioRol."""

from typing import Optional, List
from datetime import datetime
from sqlmodel import Field, Relationship, SQLModel


class UsuarioRolLink(SQLModel, table=True):
    """Tabla junction para relación many-to-many entre Usuario y Rol."""
    __tablename__ = "usuario_rol"

    usuario_id: Optional[int] = Field(default=None, foreign_key="usuario.id", primary_key=True)
    rol_codigo: Optional[str] = Field(default=None, foreign_key="rol.codigo", primary_key=True)


class RolBase(SQLModel):
    descripcion: str = Field(max_length=100)


class Rol(RolBase, table=True):
    """Roles del sistema: ADMIN, STOCK, PEDIDOS, CLIENT."""
    codigo: str = Field(primary_key=True, max_length=20)
    usuarios: List["Usuario"] = Relationship(back_populates="roles", link_model=UsuarioRolLink)


class UsuarioBase(SQLModel):
    nombre: str = Field(max_length=100)
    email: str = Field(index=True, unique=True, max_length=100)


class Usuario(UsuarioBase, table=True):
    """Usuario del sistema con roles asociados."""
    id: Optional[int] = Field(default=None, primary_key=True)
    password_hash: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    deleted_at: Optional[datetime] = None

    # Relación many-to-many con Rol
    roles: List[Rol] = Relationship(back_populates="usuarios", link_model=UsuarioRolLink)
