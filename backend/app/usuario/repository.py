"""Repository para Usuario."""

from typing import Optional, List
from sqlmodel import Session, select
from app.core.repository import BaseRepository
from app.usuario.model import Usuario


class UsuarioRepository(BaseRepository[Usuario]):
    """Repository especializado para Usuario."""

    def __init__(self, session: Session):
        super().__init__(session, Usuario)

    def get_by_email(self, email: str) -> Optional[Usuario]:
        """Obtiene un usuario por email."""
        statement = select(self.model).where(self.model.email == email)
        return self.session.exec(statement).first()

    def get_all_paginado(self, rol_codigo: Optional[str] = None, limit: int = 100, offset: int = 0) -> tuple[List[Usuario], int]:
        """Obtiene usuarios paginados, opcionalmente filtrando por rol."""
        # Query base
        statement = select(self.model)

        # Filtrar por rol si se proporciona
        if rol_codigo:
            statement = statement.join(self.model.roles).where(
                self.model.roles.any(lambda r: r.codigo == rol_codigo)
            )

        # Contar total
        count_statement = select(self.model)
        if rol_codigo:
            count_statement = count_statement.join(self.model.roles).where(
                self.model.roles.any(lambda r: r.codigo == rol_codigo)
            )
        total = len(self.session.exec(count_statement).all())

        # Aplicar paginación
        statement = statement.offset(offset).limit(limit)
        items = self.session.exec(statement).all()

        return items, total
