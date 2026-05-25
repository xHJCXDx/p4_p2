from typing import List, Optional, Tuple
from sqlmodel import Session
from app.core.repository import BaseRepository
from app.ingrediente.model import Ingrediente


class IngredienteRepository(BaseRepository[Ingrediente]):
    """Repository for Ingrediente entity"""

    def __init__(self, session: Session):
        super().__init__(session, Ingrediente)

    def get_all(self, limit: int = 100, offset: int = 0) -> Tuple[List[Ingrediente], int]:
        """Get all ingredientes with pagination"""
        return super().get_all(limit, offset)

    def get_by_id(self, ingrediente_id: int) -> Optional[Ingrediente]:
        """Get ingrediente by ID"""
        return super().get_by_id(ingrediente_id)

    def create(self, ingrediente: Ingrediente) -> Ingrediente:
        """Create a new ingrediente"""
        return super().create(ingrediente)

    def update(self, db_ingrediente: Ingrediente, ingrediente_data: dict) -> Ingrediente:
        """Update an ingrediente"""
        return super().update(db_ingrediente, ingrediente_data)

    def delete(self, db_ingrediente: Ingrediente) -> None:
        """Delete an ingrediente"""
        super().delete(db_ingrediente)

    def flush(self) -> None:
        """Flush without committing"""
        self.session.flush()
