from datetime import timedelta
from fastapi import APIRouter, Depends, status, Response
from sqlmodel import Session

from app.core.database import get_session
from app.core.response import success_response, error_response, ApiResponse
from app.core.security import (
    create_access_token,
    get_current_user,
    verify_password,
    ACCESS_TOKEN_EXPIRE_MINUTES
)
from app.usuario.schema import UsuarioCreate, UsuarioLogin
from app.usuario.model import Usuario
from app.usuario import service

router = APIRouter(prefix="/api/v1/auth", tags=["Autenticación"])


@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(
    user_data: UsuarioCreate,
    session: Session = Depends(get_session)
) -> ApiResponse:
    try:
        new_user = service.register_user(session, user_data)
        return success_response(
            data=service.usuario_to_read(new_user),
            message="Usuario registrado exitosamente",
            status_code=201
        )
    except ValueError as e:
        return error_response(message=str(e), status_code=400)
    except Exception as e:
        return error_response(message=f"Error al registrar usuario: {str(e)}", status_code=400)


@router.post("/login")
def login(
    credentials: UsuarioLogin,
    response: Response,
    session: Session = Depends(get_session)
) -> ApiResponse:
    user = service.login_user(session, credentials.email, credentials.password)

    if not user:
        return error_response(
            message="Email o contraseña inválidos",
            status_code=status.HTTP_401_UNAUTHORIZED
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id)},
        expires_delta=access_token_expires
    )

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=False,
        samesite="lax",
        path="/",
        max_age=60 * ACCESS_TOKEN_EXPIRE_MINUTES
    )

    return success_response(
        data=service.usuario_to_read(user),
        message="Autenticación exitosa"
    )


@router.get("/me")
def get_me(current_user: Usuario = Depends(get_current_user)) -> ApiResponse:
    return success_response(
        data=service.usuario_to_read(current_user),
        message="Datos del usuario obtenidos"
    )


@router.post("/logout")
def logout(response: Response) -> ApiResponse:
    """
    Cierra la sesión borrando la cookie de acceso.
    """
    response.delete_cookie(key="access_token")
    return success_response(message="Sesión cerrada exitosamente")
