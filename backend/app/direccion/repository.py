"""Repository para DireccionEntrega."""

from typing import List, Optional
from sqlmodel import Session, select
from app.core.repository import BaseRepository
from app.direccion.model import DireccionEntrega


class DireccionEntregaRepository(BaseRepository[DireccionEntrega]):
    """Repository especializado para DireccionEntrega."""

    def __init__(self, session: Session):
        super().__init__(session, DireccionEntrega)

    def get_by_usuario(self, usuario_id: int, limit: int = 100, offset: int = 0) -> tuple[List[DireccionEntrega], int]:
        """Obtiene direcciones de un usuario (excluye eliminadas)."""
        statement = select(self.model).where(
            (self.model.usuario_id == usuario_id) & (self.model.deleted_at.is_(None))
        ).offset(offset).limit(limit)
        items = self.session.exec(statement).all()

        count_statement = select(self.model).where(
            (self.model.usuario_id == usuario_id) & (self.model.deleted_at.is_(None))
        )
        total = len(self.session.exec(count_statement).all())

        return items, total

    def get_principal(self, usuario_id: int) -> Optional[DireccionEntrega]:
        """Obtiene la dirección principal del usuario (excluye eliminadas)."""
        statement = select(self.model).where(
            (self.model.usuario_id == usuario_id) & (self.model.es_principal == True) & (self.model.deleted_at.is_(None))
        )
        return self.session.exec(statement).first()
