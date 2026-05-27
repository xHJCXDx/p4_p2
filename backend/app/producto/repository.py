from typing import List, Optional, Tuple
from datetime import datetime
from sqlmodel import Session, select
from app.core.repository import BaseRepository
from app.producto.model import Producto, ProductoIngredienteLink
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

    def create(self, producto: Producto, categoria_ids: List[int] = None, ingredientes_data: list = None) -> Producto:
        if categoria_ids:
            for cat_id in categoria_ids:
                categoria = self.session.get(Categoria, cat_id)
                if categoria:
                    producto.categorias.append(categoria)

        self.session.add(producto)
        self.session.flush()

        if ingredientes_data:
            for ing_data in ingredientes_data:
                ingrediente = self.session.get(Ingrediente, ing_data.ingrediente_id)
                if ingrediente:
                    link = ProductoIngredienteLink(
                        producto_id=producto.id,
                        ingrediente_id=ing_data.ingrediente_id,
                        cantidad=ing_data.cantidad,
                        es_removible=ing_data.es_removible,
                    )
                    self.session.add(link)

        self.session.flush()
        return producto

    def update(self, db_producto: Producto, producto_data: dict, categoria_ids: List[int] = None, ingredientes_data: list = None) -> Producto:
        if categoria_ids is not None:
            db_producto.categorias = []
            for cat_id in categoria_ids:
                categoria = self.session.get(Categoria, cat_id)
                if categoria:
                    db_producto.categorias.append(categoria)

        if ingredientes_data is not None:
            # Borrar links existentes
            existing_links = self.session.exec(
                select(ProductoIngredienteLink).where(
                    ProductoIngredienteLink.producto_id == db_producto.id
                )
            ).all()
            for link in existing_links:
                self.session.delete(link)
            self.session.flush()

            # Crear nuevos links con cantidad
            for ing_data in ingredientes_data:
                ingrediente = self.session.get(Ingrediente, ing_data.ingrediente_id)
                if ingrediente:
                    link = ProductoIngredienteLink(
                        producto_id=db_producto.id,
                        ingrediente_id=ing_data.ingrediente_id,
                        cantidad=ing_data.cantidad,
                        es_removible=ing_data.es_removible,
                    )
                    self.session.add(link)

        return super().update(db_producto, producto_data)

    def get_ingrediente_links(self, producto_id: int) -> List[ProductoIngredienteLink]:
        """Obtiene los links producto-ingrediente con cantidad"""
        statement = select(ProductoIngredienteLink).where(
            ProductoIngredienteLink.producto_id == producto_id
        )
        return list(self.session.exec(statement).all())

    def delete(self, db_producto: Producto) -> None:
        """Soft delete a producto"""
        db_producto.deleted_at = datetime.utcnow()
        self.session.add(db_producto)

    def flush(self) -> None:
        """Flush without committing"""
        self.session.flush()
