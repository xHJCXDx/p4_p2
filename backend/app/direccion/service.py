"""Service para DireccionEntrega."""

from typing import Tuple, List
from datetime import datetime
from sqlmodel import Session
from app.direccion.model import DireccionEntrega
from app.direccion.schema import DireccionCreate, DireccionUpdate
from app.direccion.unit_of_work import DireccionEntregaUnitOfWork


def get_direcciones_by_usuario(session: Session, usuario_id: int, limit: int = 10, offset: int = 0) -> Tuple[List[DireccionEntrega], int]:
    """Obtiene todas las direcciones de un usuario con paginación."""
    with DireccionEntregaUnitOfWork(session) as uow:
        return uow.direcciones.get_by_usuario(usuario_id, limit, offset)


def create_direccion(session: Session, usuario_id: int, data: DireccionCreate) -> DireccionEntrega:
    """Crea una nueva dirección de entrega."""
    with DireccionEntregaUnitOfWork(session) as uow:
        # Si es principal, desmarcar las otras direcciones del usuario
        if data.es_principal:
            principal_actual = uow.direcciones.get_principal(usuario_id)
            if principal_actual:
                principal_actual.es_principal = False
                session.add(principal_actual)

        # Crear nueva dirección
        nueva_direccion = DireccionEntrega(
            usuario_id=usuario_id,
            alias=data.alias,
            calle=data.calle,
            ciudad=data.ciudad,
            provincia=data.provincia,
            codigo_postal=data.codigo_postal,
            es_principal=data.es_principal
        )

        session.add(nueva_direccion)
    return nueva_direccion


def get_direccion_by_id(session: Session, direccion_id: int) -> DireccionEntrega | None:
    """Obtiene una dirección por ID."""
    return session.get(DireccionEntrega, direccion_id)


def update_direccion(session: Session, direccion: DireccionEntrega, data: DireccionUpdate) -> DireccionEntrega:
    """Actualiza una dirección."""
    with DireccionEntregaUnitOfWork(session) as uow:
        # Si se marca como principal, desmarcar las otras
        if data.es_principal and not direccion.es_principal:
            principal_actual = uow.direcciones.get_principal(direccion.usuario_id)
            if principal_actual:
                principal_actual.es_principal = False
                session.add(principal_actual)

        # Actualizar campos
        if data.alias:
            direccion.alias = data.alias
        if data.calle:
            direccion.calle = data.calle
        if data.ciudad:
            direccion.ciudad = data.ciudad
        if data.provincia:
            direccion.provincia = data.provincia
        if data.codigo_postal:
            direccion.codigo_postal = data.codigo_postal
        if data.es_principal is not None:
            direccion.es_principal = data.es_principal

        direccion.updated_at = datetime.utcnow()
        session.add(direccion)
    return direccion


def delete_direccion(session: Session, direccion: DireccionEntrega) -> None:
    """Soft delete de una dirección."""
    with DireccionEntregaUnitOfWork(session) as uow:
        direccion.deleted_at = datetime.utcnow()
        session.add(direccion)
