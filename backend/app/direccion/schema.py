"""Schemas para DireccionEntrega."""

from typing import Optional
from pydantic import BaseModel


class DireccionCreate(BaseModel):
    alias: str
    calle: str
    ciudad: str
    provincia: str
    codigo_postal: str
    es_principal: Optional[bool] = False


class DireccionRead(BaseModel):
    id: int
    usuario_id: int
    alias: str
    calle: str
    ciudad: str
    provincia: str
    codigo_postal: str
    es_principal: bool
    created_at: str


class DireccionUpdate(BaseModel):
    alias: Optional[str] = None
    calle: Optional[str] = None
    ciudad: Optional[str] = None
    provincia: Optional[str] = None
    codigo_postal: Optional[str] = None
