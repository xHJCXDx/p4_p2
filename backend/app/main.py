from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, select
from app.core.database import create_db_and_tables, engine
from app.core.constants import ROLES
from app.core.security import hash_password
from app.categoria.router import router as categoria_router
from app.producto.router import router as producto_router
from app.ingrediente.router import router as ingrediente_router
from app.venta.router import router as venta_router
from app.usuario.router import router as auth_router
from app.usuario.model import Rol, Usuario
from app.direccion.router import router as direccion_router
from app.admin.router import router as admin_router
from app.catalogo.service import seed_catalogos
from app.seed import seed_data_completo


def seed_roles(session: Session):
    """Seed de roles obligatorios."""
    for role_data in ROLES:
        existing = session.exec(select(Rol).where(Rol.codigo == role_data["codigo"])).first()
        if not existing:
            new_role = Rol(codigo=role_data["codigo"], descripcion=role_data["descripcion"])
            session.add(new_role)
    session.commit()


def seed_users(session: Session):
    """Seed de usuarios por defecto para cada rol."""
    from app.usuario.model import UsuarioRolLink

    users_data = [
        {"nombre": "Admin", "email": "admin@admin.com", "password": "admin123", "rol": "ADMIN"},
        {"nombre": "Cliente Demo", "email": "cliente@test.com", "password": "cliente123", "rol": "CLIENT"},
        {"nombre": "Empleado Pedidos", "email": "empleado@cafe.com", "password": "empleado123", "rol": "PEDIDOS"},
        {"nombre": "Gerente Stock", "email": "gerente@cafe.com", "password": "gerente123", "rol": "STOCK"},
    ]

    for user_data in users_data:
        existing = session.exec(select(Usuario).where(Usuario.email == user_data["email"])).first()
        if not existing:
            user = Usuario(
                nombre=user_data["nombre"],
                email=user_data["email"],
                password_hash=hash_password(user_data["password"])
            )
            session.add(user)
            session.flush()

            role = session.exec(select(Rol).where(Rol.codigo == user_data["rol"])).first()
            if role:
                usuario_rol = UsuarioRolLink(usuario_id=user.id, rol_codigo=role.codigo)
                session.add(usuario_rol)

    session.commit()


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    with Session(engine) as session:
        seed_roles(session)
        seed_catalogos(session)
        seed_users(session)
        seed_data_completo(session)
    yield

app = FastAPI(lifespan=lifespan)

origins = [
    "http://localhost:5173",
    "http://localhost:5174",
    "http://localhost:5175",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(direccion_router)
app.include_router(admin_router)
app.include_router(categoria_router)
app.include_router(producto_router)
app.include_router(ingrediente_router)
app.include_router(venta_router)

@app.get("/")
def read_root():
    return {"message": "API de Productos y Categorías"}
