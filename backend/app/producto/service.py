from typing import List, Optional, Tuple
from datetime import datetime
from sqlmodel import Session
from app.producto.model import Producto
from app.producto.schema import ProductoCreate, ProductoUpdate
from app.producto.unit_of_work import ProductoUnitOfWork


def get_all(session: Session, limit: int = 100, offset: int = 0) -> Tuple[List[Producto], int]:
    with ProductoUnitOfWork(session) as uow:
        return uow.productos.get_all(limit, offset)


def get_by_id(session: Session, producto_id: int) -> Optional[Producto]:
    with ProductoUnitOfWork(session) as uow:
        return uow.productos.get_by_id(producto_id)


def create(session: Session, producto_data: ProductoCreate) -> Producto:
    with ProductoUnitOfWork(session) as uow:
        db_producto = Producto.model_validate(producto_data)
        producto = uow.productos.create(db_producto, producto_data.categoria_ids, producto_data.ingrediente_ids)
    session.refresh(producto)
    return producto


def update(session: Session, db_producto: Producto, producto_data: ProductoUpdate) -> Producto:
    with ProductoUnitOfWork(session) as uow:
        producto_dict = producto_data.model_dump(exclude_unset=True)

        categoria_ids = producto_dict.pop("categoria_ids", None)
        ingrediente_ids = producto_dict.pop("ingrediente_ids", None)

        producto_dict["updated_at"] = datetime.utcnow()

        updated = uow.productos.update(db_producto, producto_dict, categoria_ids, ingrediente_ids)
    session.refresh(updated)
    return updated


def delete(session: Session, db_producto: Producto):
    with ProductoUnitOfWork(session) as uow:
        uow.productos.delete(db_producto)
