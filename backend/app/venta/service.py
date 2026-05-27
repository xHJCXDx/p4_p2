from typing import List, Optional, Tuple
from datetime import datetime
from sqlmodel import Session
from app.venta.model import Pedido, DetallePedido, Pago, HistorialEstadoPedido
from app.venta.schema import PedidoCreate, PedidoCreateFromCheckout, PedidoUpdate, DetallePedidoCreate, PagoCreate
from app.venta.unit_of_work import VentaUnitOfWork
from app.core.constants import TRANSICIONES_PERMITIDAS
from app.producto.model import Producto, ProductoIngredienteLink
from app.ingrediente.model import Ingrediente


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


def create_pedido_from_checkout(session: Session, checkout_data: PedidoCreateFromCheckout, usuario_id: int) -> Pedido:
    """
    Crea pedido completo desde el checkout del cliente.
    Valida stock de ingredientes, calcula totales, crea detalles con snapshot,
    y descuenta stock de los ingredientes.
    """
    if not checkout_data.linea_ventas:
        raise ValueError("El pedido debe tener al menos un producto")

    from sqlmodel import select

    # Validar stock de ingredientes y calcular subtotal
    subtotal = 0.0
    productos_info = []
    # Acumular consumo total de cada ingrediente para validar ANTES de descontar
    consumo_ingredientes: dict[int, int] = {}

    for linea in checkout_data.linea_ventas:
        producto = session.get(Producto, linea.producto_id)
        if not producto or producto.deleted_at is not None:
            raise ValueError(f"Producto {linea.producto_id} no existe o fue eliminado")

        # Obtener receta del producto
        links = session.exec(
            select(ProductoIngredienteLink).where(
                ProductoIngredienteLink.producto_id == producto.id
            )
        ).all()

        # Acumular consumo de ingredientes
        for link in links:
            total_necesario = link.cantidad * linea.cantidad
            consumo_ingredientes[link.ingrediente_id] = (
                consumo_ingredientes.get(link.ingrediente_id, 0) + total_necesario
            )

        linea_subtotal = producto.precio_base * linea.cantidad
        subtotal += linea_subtotal
        productos_info.append((producto, linea.cantidad, linea_subtotal))

    # Validar que hay stock suficiente de cada ingrediente
    for ing_id, cantidad_necesaria in consumo_ingredientes.items():
        ingrediente = session.get(Ingrediente, ing_id)
        if not ingrediente or ingrediente.deleted_at is not None:
            raise ValueError(f"Ingrediente {ing_id} no existe o fue eliminado")
        if ingrediente.stock_cantidad < cantidad_necesaria:
            raise ValueError(
                f"Stock insuficiente de ingrediente '{ingrediente.nombre}': "
                f"disponible {ingrediente.stock_cantidad}, necesario {cantidad_necesaria}"
            )

    costo_envio = 50.0
    total = subtotal + costo_envio

    with VentaUnitOfWork(session) as uow:
        pedido = Pedido(
            usuario_id=usuario_id,
            direccion_id=checkout_data.direccion_id,
            estado_codigo="PENDIENTE",
            forma_pago_codigo=checkout_data.forma_pago_codigo,
            notas=checkout_data.notas,
            subtotal=subtotal,
            descuento=0.0,
            costo_envio=costo_envio,
            total=total,
        )
        pedido = uow.pedidos.create(pedido)
        uow.pedidos.flush()

        # Crear detalles con snapshot
        for producto, cantidad, linea_subtotal in productos_info:
            detalle = DetallePedido(
                pedido_id=pedido.id,
                producto_id=producto.id,
                cantidad=cantidad,
                nombre_snapshot=producto.nombre,
                precio_snapshot=producto.precio_base,
                subtotal_snap=linea_subtotal,
            )
            uow.detalles.create(detalle)

        # Descontar stock de ingredientes
        for ing_id, cantidad_necesaria in consumo_ingredientes.items():
            ingrediente = session.get(Ingrediente, ing_id)
            ingrediente.stock_cantidad -= cantidad_necesaria
            session.add(ingrediente)

        # Historial inicial
        historial = HistorialEstadoPedido(
            pedido_id=pedido.id,
            estado_desde=None,
            estado_hacia="PENDIENTE",
            usuario_id=usuario_id,
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
