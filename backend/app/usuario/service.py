from typing import Optional, Tuple, List
from sqlmodel import Session, select
from app.usuario.model import Usuario, Rol, UsuarioRolLink
from app.usuario.schema import UsuarioCreate, UsuarioUpdate, UsuarioRead
from app.core.security import hash_password, verify_password
from app.usuario.unit_of_work import UsuarioUnitOfWork


def usuario_to_read(usuario: Usuario) -> UsuarioRead:
    return UsuarioRead(
        id=usuario.id,
        nombre=usuario.nombre,
        apellido=usuario.apellido,
        email=usuario.email,
        celular=usuario.celular,
        roles=[{"codigo": r.codigo, "nombre": r.nombre, "descripcion": r.descripcion} for r in usuario.roles],
        created_at=usuario.created_at.isoformat()
    )


def get_all_paginado(session: Session, limit: int = 10, offset: int = 0, rol_codigo: Optional[str] = None) -> Tuple[List[Usuario], int]:
    """Obtiene usuarios paginados, opcionalmente filtrando por rol."""
    with UsuarioUnitOfWork(session) as uow:
        if rol_codigo:
            return uow.usuarios.get_all_paginado(rol_codigo=rol_codigo, limit=limit, offset=offset)
        return uow.usuarios.get_all_paginado(limit=limit, offset=offset)


def register_user(session: Session, user_data: UsuarioCreate) -> Usuario:
    """
    Registra un nuevo usuario y le asigna el rol CLIENT automáticamente.
    """
    with UsuarioUnitOfWork(session) as uow:
        existing_user = uow.usuarios.get_by_email(user_data.email)
        if existing_user:
            raise ValueError(f"El email {user_data.email} ya está registrado")

        new_user = Usuario(
            nombre=user_data.nombre,
            apellido=user_data.apellido,
            email=user_data.email,
            celular=user_data.celular,
            password_hash=hash_password(user_data.password)
        )

        session.add(new_user)
        session.flush()

        rol_client = session.exec(select(Rol).where(Rol.codigo == "CLIENT")).first()
        if rol_client:
            usuario_rol = UsuarioRolLink(usuario_id=new_user.id, rol_codigo=rol_client.codigo)
            session.add(usuario_rol)
    return new_user


def login_user(session: Session, email: str, password: str) -> Optional[Usuario]:
    """
    Autentica un usuario con email y contraseña.
    Retorna el usuario si las credenciales son correctas, None en caso contrario.
    """
    with UsuarioUnitOfWork(session) as uow:
        user = uow.usuarios.get_by_email(email)

        if not user or not verify_password(password, user.password_hash):
            return None

        return user


def get_user_by_id(session: Session, user_id: int) -> Optional[Usuario]:
    """Obtiene un usuario por ID."""
    return session.get(Usuario, user_id)


def update_user(session: Session, user: Usuario, update_data: UsuarioUpdate) -> Usuario:
    """Actualiza datos del usuario (nombre, email)."""
    with UsuarioUnitOfWork(session) as uow:
        if update_data.email and update_data.email != user.email:
            existing = uow.usuarios.get_by_email(update_data.email)
            if existing:
                raise ValueError(f"El email {update_data.email} ya está en uso")

        if update_data.nombre:
            user.nombre = update_data.nombre
        if update_data.apellido is not None:
            user.apellido = update_data.apellido
        if update_data.email:
            user.email = update_data.email
        if update_data.celular is not None:
            user.celular = update_data.celular

        session.add(user)
    return user
