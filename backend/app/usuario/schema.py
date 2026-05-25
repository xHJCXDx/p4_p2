"""Schemas Pydantic para Usuario."""

from typing import Optional, List
from pydantic import BaseModel, EmailStr


class RolRead(BaseModel):
    """Schema para leer un Rol."""
    codigo: str
    descripcion: str


class UsuarioCreate(BaseModel):
    """Schema para crear un nuevo usuario."""
    nombre: str
    email: EmailStr
    password: str


class UsuarioLogin(BaseModel):
    """Schema para login."""
    email: EmailStr
    password: str


class UsuarioRead(BaseModel):
    """Schema para leer datos del usuario."""
    id: int
    nombre: str
    email: str
    roles: List[RolRead] = []
    created_at: str


class UsuarioUpdate(BaseModel):
    """Schema para actualizar usuario."""
    nombre: Optional[str] = None
    email: Optional[EmailStr] = None
