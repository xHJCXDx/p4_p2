from typing import List, Optional, Tuple
from datetime import datetime
from sqlmodel import Session, select
from app.core.repository import BaseRepository
from app.categoria.model import Categoria


class CategoriaRepository(BaseRepository[Categoria]):
    """Repository for Categoria entity with soft delete support"""

    def __init__(self, session: Session):
        super().__init__(session, Categoria)

    def get_all(self, limit: int = 100, offset: int = 0) -> Tuple[List[Categoria], int]:
        """Get all categorias (excluding soft-deleted) with pagination"""
        statement = select(Categoria).where(Categoria.deleted_at.is_(None)).offset(offset).limit(limit)
        items = self.session.exec(statement).all()

        # Count total (excluding soft-deleted)
        count_statement = select(Categoria).where(Categoria.deleted_at.is_(None))
        total = len(self.session.exec(count_statement).all())

        return items, total

    def get_by_id(self, categoria_id: int) -> Optional[Categoria]:
        """Get categoria by ID (returns None if soft-deleted)"""
        categoria = self.session.get(Categoria, categoria_id)
        if categoria and categoria.deleted_at is not None:
            return None
        return categoria

    def create(self, categoria: Categoria) -> Categoria:
        """Create a new categoria"""
        return super().create(categoria)

    def update(self, db_categoria: Categoria, categoria_data: dict) -> Categoria:
        """Update a categoria"""
        return super().update(db_categoria, categoria_data)

    def delete(self, db_categoria: Categoria) -> None:
        """Soft delete a categoria"""
        db_categoria.deleted_at = datetime.utcnow()
        self.session.add(db_categoria)

    def flush(self) -> None:
        """Flush without committing"""
        self.session.flush()
