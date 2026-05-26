from typing import List, Optional, Tuple
from datetime import datetime
from sqlmodel import Session, select
from app.core.repository import BaseRepository
from app.producto.model import Producto
from app.categoria.model import Categoria
from app.ingrediente.model import Ingrediente


class ProductoRepository(BaseRepository[Producto]):
    """Repository for Producto entity with soft delete support"""

    def __init__(self, session: Session):
        super().__init__(session, Producto)

    def get_all(self, limit: int = 100, offset: int = 0) -> Tuple[List[Producto], int]:
        """Get all productos (excluding soft-deleted) with pagination"""
        statement = select(Producto).where(Producto.deleted_at.is_(None)).offset(offset).limit(limit)
        items = self.session.exec(statement).all()

        # Count total (excluding soft-deleted)
        count_statement = select(Producto).where(Producto.deleted_at.is_(None))
        total = len(self.session.exec(count_statement).all())

        return items, total

    def get_by_id(self, producto_id: int) -> Optional[Producto]:
        """Get producto by ID (returns None if soft-deleted)"""
        producto = self.session.get(Producto, producto_id)
        if producto and producto.deleted_at is not None:
            return None
        return producto

    def create(self, producto: Producto, categoria_ids: List[int] = None, ingrediente_ids: List[int] = None) -> Producto:
        if categoria_ids:
            for cat_id in categoria_ids:
                categoria = self.session.get(Categoria, cat_id)
                if categoria:
                    producto.categorias.append(categoria)

        if ingrediente_ids:
            for ing_id in ingrediente_ids:
                ingrediente = self.session.get(Ingrediente, ing_id)
                if ingrediente:
                    producto.ingredientes.append(ingrediente)

        return super().create(producto)

    def update(self, db_producto: Producto, producto_data: dict, categoria_ids: List[int] = None, ingrediente_ids: List[int] = None) -> Producto:
        if categoria_ids is not None:
            db_producto.categorias = []
            for cat_id in categoria_ids:
                categoria = self.session.get(Categoria, cat_id)
                if categoria:
                    db_producto.categorias.append(categoria)

        if ingrediente_ids is not None:
            db_producto.ingredientes = []
            for ing_id in ingrediente_ids:
                ingrediente = self.session.get(Ingrediente, ing_id)
                if ingrediente:
                    db_producto.ingredientes.append(ingrediente)

        return super().update(db_producto, producto_data)

    def delete(self, db_producto: Producto) -> None:
        """Soft delete a producto"""
        db_producto.deleted_at = datetime.utcnow()
        self.session.add(db_producto)

    def flush(self) -> None:
        """Flush without committing"""
        self.session.flush()
