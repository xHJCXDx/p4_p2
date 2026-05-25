from datetime import datetime
from typing import Optional
from fastapi import APIRouter, Depends, status, Query
from sqlmodel import Session, select
from app.core.database import get_session
from app.core.response import success_response, error_response, ApiResponse
from app.core.security import require_roles
from app.usuario.model import Usuario, Rol, UsuarioRolLink
from app.usuario.schema import UsuarioUpdate
from app.usuario import service as usuario_service

router = APIRouter(prefix="/api/v1/admin", tags=["Admin"])


@router.get("/usuarios", dependencies=[Depends(require_roles("ADMIN"))])
def listar_usuarios(
    session: Session = Depends(get_session),
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    rol: Optional[str] = Query(None, description="Filtrar por rol")
) -> ApiResponse:
    usuarios, total = usuario_service.get_all_paginado(session, limit=limit, offset=offset, rol_codigo=rol)

    return success_response(
        data={
            "items": [usuario_service.usuario_to_read(u) for u in usuarios],
            "total": total,
            "limit": limit,
            "offset": offset
        },
        message="Usuarios listados"
    )


@router.put("/usuarios/{usuario_id}", dependencies=[Depends(require_roles("ADMIN"))])
def actualizar_usuario(
    usuario_id: int,
    data: UsuarioUpdate,
    session: Session = Depends(get_session)
) -> ApiResponse:
    usuario = session.get(Usuario, usuario_id)
    if not usuario:
        return error_response(message="Usuario no encontrado", status_code=404)

    try:
        if data.nombre:
            usuario.nombre = data.nombre
        if data.email:
            usuario.email = data.email

        session.add(usuario)
        session.commit()

        return success_response(
            data=usuario_service.usuario_to_read(usuario),
            message="Usuario actualizado"
        )
    except Exception as e:
        return error_response(message=f"Error: {str(e)}", status_code=400)


@router.delete("/usuarios/{usuario_id}", dependencies=[Depends(require_roles("ADMIN"))])
def eliminar_usuario(
    usuario_id: int,
    session: Session = Depends(get_session)
) -> ApiResponse:
    usuario = session.get(Usuario, usuario_id)
    if not usuario:
        return error_response(message="Usuario no encontrado", status_code=404)

    usuario.deleted_at = datetime.utcnow()
    session.add(usuario)
    session.commit()

    return success_response(message="Usuario eliminado", status_code=204)


@router.post("/usuarios/{usuario_id}/roles", dependencies=[Depends(require_roles("ADMIN"))])
def asignar_rol(
    usuario_id: int,
    rol_codigo: str = Query(...),
    session: Session = Depends(get_session)
) -> ApiResponse:
    usuario = session.get(Usuario, usuario_id)
    if not usuario:
        return error_response(message="Usuario no encontrado", status_code=404)

    rol = session.get(Rol, rol_codigo)
    if not rol:
        return error_response(message="Rol no encontrado", status_code=404)

    existing = session.exec(
        select(UsuarioRolLink).where(
            (UsuarioRolLink.usuario_id == usuario_id) & (UsuarioRolLink.rol_codigo == rol_codigo)
        )
    ).first()

    if existing:
        return error_response(message="El usuario ya tiene este rol", status_code=400)

    try:
        usuario_rol = UsuarioRolLink(usuario_id=usuario_id, rol_codigo=rol_codigo)
        session.add(usuario_rol)
        session.commit()

        usuario = session.get(Usuario, usuario_id)
        return success_response(
            data=usuario_service.usuario_to_read(usuario),
            message="Rol asignado",
            status_code=201
        )
    except Exception as e:
        return error_response(message=f"Error: {str(e)}", status_code=400)
