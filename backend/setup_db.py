#!/usr/bin/env python3
"""
Script para resetear y recrear la BD con seed data completo.
Ejecutar desde el directorio raíz del backend:

    python setup_db.py

Esto:
1. Elimina la BD anterior (database.db)
2. Crea una BD nueva
3. Seedea todo (roles, catálogos, admin, categorías, ingredientes, productos)
"""

import os
import sys
from pathlib import Path

# Agregar el directorio actual al path
sys.path.insert(0, str(Path(__file__).parent))

from sqlmodel import Session
from app.core.database import create_db_and_tables, engine
from app.core.constants import ROLES
from app.usuario.model import Rol, Usuario
from app.core.security import hash_password
from app.catalogo.service import seed_catalogos
from app.seed import seed_data_completo
from sqlmodel import select


def reset_database():
    """Elimina la BD anterior si existe."""
    db_file = "database.db"
    if os.path.exists(db_file):
        print(f"🗑️  Eliminando {db_file}...")
        os.remove(db_file)
        print("✅ Base de datos anterior eliminada")


def seed_roles(session: Session):
    """Seed de roles obligatorios."""
    print("🌱 Seeding roles...")
    for role_data in ROLES:
        existing = session.exec(select(Rol).where(Rol.codigo == role_data["codigo"])).first()
        if not existing:
            new_role = Rol(codigo=role_data["codigo"], descripcion=role_data["descripcion"])
            session.add(new_role)
    session.commit()
    print(f"✅ {len(ROLES)} roles seeded")


def seed_admin_user(session: Session):
    """Seed de usuario admin por defecto."""
    print("🌱 Seeding usuario admin...")
    admin_email = "admin@admin.com"
    existing_admin = session.exec(select(Usuario).where(Usuario.email == admin_email)).first()
    if not existing_admin:
        admin_user = Usuario(
            nombre="Admin",
            email=admin_email,
            password_hash=hash_password("admin123")
        )
        session.add(admin_user)
        session.flush()

        # Asignar rol ADMIN
        admin_role = session.exec(select(Rol).where(Rol.codigo == "ADMIN")).first()
        if admin_role:
            from app.usuario.model import UsuarioRolLink
            usuario_rol = UsuarioRolLink(usuario_id=admin_user.id, rol_codigo=admin_role.codigo)
            session.add(usuario_rol)

        session.commit()
        print("✅ Usuario admin creado")
        print(f"   Email: {admin_email}")
        print(f"   Password: admin123")
    else:
        print("ℹ️  Usuario admin ya existe")


def main():
    """Flujo principal de setup."""
    print("\n" + "="*60)
    print("🚀 SETUP DE BASE DE DATOS - Parcial 2")
    print("="*60 + "\n")

    try:
        # Paso 1: Reset
        reset_database()
        print()

        # Paso 2: Crear tablas
        print("🏗️  Creando tablas...")
        create_db_and_tables()
        print("✅ Tablas creadas")
        print()

        # Paso 3: Seed data
        with Session(engine) as session:
            seed_roles(session)
            print()

            seed_catalogos(session)
            print()

            seed_admin_user(session)
            print()

            seed_data_completo(session)
            print()

        print("="*60)
        print("✅ SETUP COMPLETADO EXITOSAMENTE")
        print("="*60)
        print("\n🎉 BD lista para la demo!")
        print("   • Admin: admin@admin.com / admin123")
        print("   • Categorías: Pizzas, Empanadas, Bebidas")
        print("   • Productos: 7 productos con ingredientes")
        print("   • Ingredientes: 10 ingredientes (algunos con alergenos)")
        print()
        print("Para iniciar el servidor:")
        print("   fastapi dev main.py")
        print()

    except Exception as e:
        print(f"\n❌ ERROR EN SETUP: {str(e)}")
        print("Trace completo:")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
