from typing import Optional
from app.catalogo.model import FormaPagoBase, EstadoPedidoBase

class FormaPagoCreate(FormaPagoBase):
    codigo: str

class FormaPagoRead(FormaPagoBase):
    codigo: str

class EstadoPedidoCreate(EstadoPedidoBase):
    codigo: str

class EstadoPedidoRead(EstadoPedidoBase):
    codigo: str
