from typing import List, Optional
from datetime import datetime
from sqlmodel import Field, Relationship, SQLModel, JSON

# ============ PEDIDO ============
class PedidoBase(SQLModel):
    usuario_id: int  # FK a Usuario (aún no implementado)
    direccion_id: Optional[int] = None  # FK a DireccionEntrega (aún no implementado)
    estado_codigo: str = Field(foreign_key="estadopedido.codigo")
    forma_pago_codigo: str = Field(foreign_key="formapago.codigo")
    notas: Optional[str] = None

class Pedido(PedidoBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    # Snapshot monetario (immutable)
    subtotal: float = Field(ge=0)
    descuento: float = Field(default=0.0, ge=0)
    costo_envio: float = Field(default=50.0, ge=0)
    total: float = Field(ge=0)

    # Audit
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    deleted_at: Optional[datetime] = None

    # Relaciones
    detalles: List["DetallePedido"] = Relationship(back_populates="pedido", cascade_delete=True)
    pagos: List["Pago"] = Relationship(back_populates="pedido", cascade_delete=True)
    historial: List["HistorialEstadoPedido"] = Relationship(back_populates="pedido", cascade_delete=False)

# ============ DETALLE PEDIDO ============
class DetallePedidoBase(SQLModel):
    pedido_id: int = Field(foreign_key="pedido.id")
    producto_id: int = Field(foreign_key="producto.id")
    cantidad: int = Field(ge=1)
    personalizacion: List[int] = Field(default=[], sa_type=JSON)

class DetallePedido(DetallePedidoBase, table=True):
    # PK compuesta: (pedido_id, producto_id)
    pedido_id: int = Field(foreign_key="pedido.id", primary_key=True)
    producto_id: int = Field(foreign_key="producto.id", primary_key=True)

    # Snapshots (immutable)
    nombre_snapshot: str = Field(max_length=200)
    precio_snapshot: float = Field(ge=0)
    subtotal_snap: float = Field(ge=0)

    # Audit (immutable: solo created_at, sin updated_at)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relación
    pedido: Optional[Pedido] = Relationship(back_populates="detalles")

# ============ PAGO ============
class PagoBase(SQLModel):
    pedido_id: int = Field(foreign_key="pedido.id")
    mp_status: str = Field(max_length=30)
    transaction_amount: float = Field(ge=0)

class Pago(PagoBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    # MercadoPago fields
    mp_payment_id: Optional[int] = Field(default=None, unique=True)
    mp_status_detail: Optional[str] = Field(default=None, max_length=100)
    external_reference: str = Field(unique=True, max_length=100)
    idempotency_key: str = Field(unique=True, max_length=100)
    payment_method_id: Optional[str] = Field(default=None, max_length=50)

    # Audit
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relación
    pedido: Optional[Pedido] = Relationship(back_populates="pagos")

# ============ HISTORIAL ESTADO PEDIDO ============
class HistorialEstadoPedidoBase(SQLModel):
    pedido_id: int = Field(foreign_key="pedido.id")
    estado_hacia: str = Field(foreign_key="estadopedido.codigo", max_length=20)
    estado_desde: Optional[str] = Field(default=None, foreign_key="estadopedido.codigo", max_length=20)
    usuario_id: Optional[int] = None  # FK a Usuario (NULL = sistema)
    motivo: Optional[str] = None

class HistorialEstadoPedido(HistorialEstadoPedidoBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    # Audit (append-only: solo created_at)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relación
    pedido: Optional[Pedido] = Relationship(back_populates="historial")
