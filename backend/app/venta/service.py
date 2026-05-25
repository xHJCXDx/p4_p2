from typing import List, Optional, Tuple
from datetime import datetime
from sqlmodel import Session
from app.venta.model import Pedido, DetallePedido, Pago, HistorialEstadoPedido
from app.venta.schema import PedidoCreate, PedidoUpdate, DetallePedidoCreate, PagoCreate
from app.venta.unit_of_work import VentaUnitOfWork
from app.core.constants import TRANSICIONES_PERMITIDAS
from app.producto.model import Producto


# ============ PEDIDO SERVICE ============
def get_all_pedidos(session: Session, limit: int = 10, offset: int = 0, usuario_id: Optional[int] = None) -> Tuple[List[Pedido], int]:
    """
    Obtiene pedidos con paginación, excluyendo soft-deleted.
    Si usuario_id es provided, filtra solo los pedidos de ese usuario (CLIENT).
    Si usuario_id es None, devuelve todos (ADMIN/PEDIDOS).
    """
    with VentaUnitOfWork(session) as uow:
        if usuario_id:
            return uow.pedidos.get_all_for_user(usuario_id, limit, offset)
        return uow.pedidos.get_all(limit, offset)


def get_pedido_by_id(session: Session, pedido_id: int) -> Optional[Pedido]:
    """Obtiene un pedido por ID, retorna None si está deleted o no existe."""
    with VentaUnitOfWork(session) as uow:
        return uow.pedidos.get_by_id(pedido_id)


def create_pedido(session: Session, pedido_data: PedidoCreate) -> Pedido:
    """Crea un nuevo pedido e inserta el primer registro en HistorialEstadoPedido."""
    with VentaUnitOfWork(session) as uow:
        new_pedido = Pedido.model_validate(pedido_data)
        pedido = uow.pedidos.create(new_pedido)
        uow.pedidos.flush()  # Asegura que get id antes de commit

        # Crear historial inicial (RN-02: estado_desde debe ser NULL en la creación)
        historial = HistorialEstadoPedido(
            pedido_id=pedido.id,
            estado_desde=None,
            estado_hacia=pedido.estado_codigo,
            usuario_id=None,
            motivo=None
        )
        uow.historial.create(historial)
    session.refresh(pedido)
    return pedido


def update_pedido(session: Session, db_pedido: Pedido, pedido_data: PedidoUpdate) -> Pedido:
    """Actualiza un pedido (sin cambiar estado; usar transition_estado para eso)."""
    with VentaUnitOfWork(session) as uow:
        update_dict = pedido_data.model_dump(exclude_unset=True)
        updated = uow.pedidos.update(db_pedido, update_dict)
    session.refresh(updated)
    return updated


def delete_pedido(session: Session, db_pedido: Pedido):
    """Soft delete: marca con deleted_at."""
    with VentaUnitOfWork(session) as uow:
        uow.pedidos.delete(db_pedido)


def transition_estado(
    session: Session,
    pedido_id: int,
    nuevo_estado: str,
    usuario_id: Optional[int] = None,
    motivo: Optional[str] = None
) -> Pedido:
    """
    Realiza transición de estado con validaciones de FSM.
    RN-01: Valida si transición es permitida.
    RN-05: Valida motivo obligatorio si el nuevo estado es CANCELADO.
    """
    with VentaUnitOfWork(session) as uow:
        pedido = uow.pedidos.get_by_id(pedido_id)
        if not pedido:
            raise ValueError(f"Pedido {pedido_id} no encontrado")

        estado_actual = pedido.estado_codigo
        transiciones_validas = TRANSICIONES_PERMITIDAS.get(estado_actual, [])

        # Validación de transición
        if nuevo_estado not in transiciones_validas:
            raise ValueError(
                f"Transición no permitida: {estado_actual} → {nuevo_estado}. "
                f"Transiciones permitidas: {transiciones_validas}"
            )

        # RN-05: motivo obligatorio para CANCELADO
        if nuevo_estado == "CANCELADO" and not motivo:
            raise ValueError("Motivo obligatorio para cancelar un pedido")

        # Actualizar estado del pedido
        updated_pedido = uow.pedidos.update_estado(pedido, nuevo_estado)

        # Insertar en historial
        historial = HistorialEstadoPedido(
            pedido_id=pedido_id,
            estado_desde=estado_actual,
            estado_hacia=nuevo_estado,
            usuario_id=usuario_id,
            motivo=motivo
        )
        uow.historial.create(historial)
    session.refresh(updated_pedido)
    return updated_pedido


# ============ DETALLE PEDIDO SERVICE ============
def get_detalles_by_pedido(session: Session, pedido_id: int) -> List[DetallePedido]:
    """Obtiene todos los detalles de un pedido."""
    with VentaUnitOfWork(session) as uow:
        return uow.detalles.get_by_pedido(pedido_id)


def create_detalle_pedido(session: Session, detalle_data: DetallePedidoCreate) -> DetallePedido:
    """Crea un detalle de pedido (immutable después de creación)."""
    # Validar que el producto existe
    producto = session.get(Producto, detalle_data.producto_id)
    if not producto or producto.deleted_at is not None:
        raise ValueError(f"Producto {detalle_data.producto_id} no existe o ha sido eliminado")

    with VentaUnitOfWork(session) as uow:
        new_detalle = DetallePedido.model_validate(detalle_data)
        detalle = uow.detalles.create(new_detalle)
    session.refresh(detalle)
    return detalle


# ============ PAGO SERVICE ============
def get_pagos_by_pedido(session: Session, pedido_id: int) -> List[Pago]:
    """Obtiene todos los pagos de un pedido."""
    with VentaUnitOfWork(session) as uow:
        return uow.pagos.get_by_pedido(pedido_id)


def get_pago_by_id(session: Session, pago_id: int) -> Optional[Pago]:
    """Obtiene un pago por ID."""
    with VentaUnitOfWork(session) as uow:
        return uow.pagos.get_by_id(pago_id)


def create_pago(session: Session, pago_data: PagoCreate) -> Pago:
    """Crea un registro de pago."""
    # Validar que el pedido existe
    pedido = session.get(Pedido, pago_data.pedido_id)
    if not pedido or pedido.deleted_at is not None:
        raise ValueError(f"Pedido {pago_data.pedido_id} no existe o ha sido eliminado")

    with VentaUnitOfWork(session) as uow:
        new_pago = Pago.model_validate(pago_data)
        pago = uow.pagos.create(new_pago)
    session.refresh(pago)
    return pago


def update_pago(session: Session, db_pago: Pago, pago_data: dict) -> Pago:
    """Actualiza un pago (para cambios de estado MP)."""
    with VentaUnitOfWork(session) as uow:
        update_dict = {k: v for k, v in pago_data.items() if v is not None}
        updated = uow.pagos.update(db_pago, update_dict)
    session.refresh(updated)
    return updated
