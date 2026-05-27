"""Seed data completo para el Parcial 2 (categorías, ingredientes, productos)."""

from sqlmodel import Session, select
from app.categoria.model import Categoria
from app.ingrediente.model import Ingrediente
from app.producto.model import Producto, ProductoCategoriaLink, ProductoIngredienteLink


def seed_data_completo(session: Session) -> None:
    """
    Seedea categorías, ingredientes y productos si no existen.
    Se ejecuta una sola vez al iniciar la app.
    """

    # ============ INGREDIENTES ============
    def seed_ingredientes():
        ingredientes_data = [
            {"nombre": "Queso Mozzarella", "descripcion": "Queso fresco derretible", "es_alergeno": False, "stock_cantidad": 200},
            {"nombre": "Tomate", "descripcion": "Tomate fresco", "es_alergeno": False, "stock_cantidad": 150},
            {"nombre": "Oregano", "descripcion": "Hierba aromática", "es_alergeno": False, "stock_cantidad": 300},
            {"nombre": "Maní", "descripcion": "Cacahuete", "es_alergeno": True, "stock_cantidad": 50},
            {"nombre": "Leche", "descripcion": "Leche fresca", "es_alergeno": True, "stock_cantidad": 100},
            {"nombre": "Huevo", "descripcion": "Huevo fresco", "es_alergeno": True, "stock_cantidad": 120},
            {"nombre": "Gluten", "descripcion": "Harina con gluten", "es_alergeno": True, "stock_cantidad": 250},
            {"nombre": "Carne molida", "descripcion": "Carne vacuna molida", "es_alergeno": False, "stock_cantidad": 100},
            {"nombre": "Cebolla", "descripcion": "Cebolla fresca", "es_alergeno": False, "stock_cantidad": 180},
            {"nombre": "Ajo", "descripcion": "Ajo fresco", "es_alergeno": False, "stock_cantidad": 200},
            {"nombre": "Coca-Cola 2L", "descripcion": "Botella de Coca-Cola 2 litros", "es_alergeno": False, "stock_cantidad": 200},
            {"nombre": "Naranja", "descripcion": "Naranja fresca para exprimir", "es_alergeno": False, "stock_cantidad": 150},
        ]

        ingredientes = {}
        for ing_data in ingredientes_data:
            existing = session.exec(
                select(Ingrediente).where(Ingrediente.nombre == ing_data["nombre"])
            ).first()
            if not existing:
                ing = Ingrediente(**ing_data)
                session.add(ing)
                session.flush()
                ingredientes[ing_data["nombre"]] = ing
            else:
                ingredientes[ing_data["nombre"]] = existing

        session.commit()
        return ingredientes

    # ============ CATEGORÍAS ============
    def seed_categorias():
        categorias_data = [
            {
                "nombre": "Pizzas",
                "descripcion": "Pizzas artesanales",
                "parent_id": None,
                "imagen_url": "https://via.placeholder.com/200?text=Pizzas"
            },
            {
                "nombre": "Empanadas",
                "descripcion": "Empanadas caseras",
                "parent_id": None,
                "imagen_url": "https://via.placeholder.com/200?text=Empanadas"
            },
            {
                "nombre": "Bebidas",
                "descripcion": "Bebidas frías y calientes",
                "parent_id": None,
                "imagen_url": "https://via.placeholder.com/200?text=Bebidas"
            },
            {
                "nombre": "Pizzas Dulces",
                "descripcion": "Pizzas de postre",
                "parent_id": 1,
                "imagen_url": "https://via.placeholder.com/200?text=Pizzas+Dulces"
            },
        ]

        categorias = {}
        for cat_data in categorias_data:
            existing = session.exec(
                select(Categoria).where(Categoria.nombre == cat_data["nombre"])
            ).first()
            if not existing:
                cat = Categoria(**cat_data)
                session.add(cat)
                session.flush()
                categorias[cat_data["nombre"]] = cat
            else:
                categorias[cat_data["nombre"]] = existing

        session.commit()
        return categorias

    # ============ PRODUCTOS ============
    def seed_productos(categorias, ingredientes):
        productos_data = [
            {
                "nombre": "Pizza Margherita",
                "descripcion": "Pizza clásica italiana con queso y tomate",
                "precio_base": 250.0,
                "categoria_id": categorias["Pizzas"].id,
                "ingredientes": [
                    {"ref": "Queso Mozzarella", "cantidad": 3, "es_removible": True},
                    {"ref": "Tomate", "cantidad": 2, "es_removible": True},
                    {"ref": "Oregano", "cantidad": 1, "es_removible": True},
                ]
            },
            {
                "nombre": "Pizza de Carne",
                "descripcion": "Pizza con carne molida, cebolla y ajo",
                "precio_base": 290.0,
                "categoria_id": categorias["Pizzas"].id,
                "ingredientes": [
                    {"ref": "Carne molida", "cantidad": 3, "es_removible": False},
                    {"ref": "Cebolla", "cantidad": 2, "es_removible": True},
                    {"ref": "Ajo", "cantidad": 1, "es_removible": True},
                    {"ref": "Queso Mozzarella", "cantidad": 2, "es_removible": True},
                ]
            },
            {
                "nombre": "Empanadas de Carne",
                "descripcion": "6 empanadas de carne casera",
                "precio_base": 120.0,
                "categoria_id": categorias["Empanadas"].id,
                "ingredientes": [
                    {"ref": "Carne molida", "cantidad": 2, "es_removible": False},
                    {"ref": "Cebolla", "cantidad": 1, "es_removible": True},
                    {"ref": "Gluten", "cantidad": 3, "es_removible": False},
                ]
            },
            {
                "nombre": "Empanadas de Queso",
                "descripcion": "6 empanadas de queso y cebolla",
                "precio_base": 100.0,
                "categoria_id": categorias["Empanadas"].id,
                "ingredientes": [
                    {"ref": "Queso Mozzarella", "cantidad": 3, "es_removible": False},
                    {"ref": "Cebolla", "cantidad": 1, "es_removible": True},
                    {"ref": "Gluten", "cantidad": 3, "es_removible": False},
                ]
            },
            {
                "nombre": "Coca-Cola 2L",
                "descripcion": "Bebida gaseosa clásica",
                "precio_base": 65.0,
                "categoria_id": categorias["Bebidas"].id,
                "ingredientes": [
                    {"ref": "Coca-Cola 2L", "cantidad": 1, "es_removible": False},
                ]
            },
            {
                "nombre": "Jugo Natural Naranja",
                "descripcion": "Jugo fresco de naranja recién exprimido",
                "precio_base": 45.0,
                "categoria_id": categorias["Bebidas"].id,
                "ingredientes": [
                    {"ref": "Naranja", "cantidad": 3, "es_removible": False},
                ]
            },
            {
                "nombre": "Pizza de Chocolate",
                "descripcion": "Pizza dulce de chocolate con frutos secos",
                "precio_base": 200.0,
                "categoria_id": categorias["Pizzas Dulces"].id,
                "ingredientes": [
                    {"ref": "Maní", "cantidad": 2, "es_removible": True},
                    {"ref": "Leche", "cantidad": 3, "es_removible": False},
                ]
            },
        ]

        productos = {}
        for prod_data in productos_data:
            existing = session.exec(
                select(Producto).where(Producto.nombre == prod_data["nombre"])
            ).first()
            if not existing:
                cat_id = prod_data.pop("categoria_id")
                ingredientes_prod = prod_data.pop("ingredientes", [])

                prod = Producto(**prod_data)
                session.add(prod)
                session.flush()

                # Asignar categoría
                link_cat = ProductoCategoriaLink(
                    producto_id=prod.id,
                    categoria_id=cat_id,
                    es_principal=True
                )
                session.add(link_cat)

                # Asignar ingredientes con cantidad
                for ing_info in ingredientes_prod:
                    ing = ingredientes[ing_info["ref"]]
                    link_ing = ProductoIngredienteLink(
                        producto_id=prod.id,
                        ingrediente_id=ing.id,
                        cantidad=ing_info["cantidad"],
                        es_removible=ing_info["es_removible"],
                    )
                    session.add(link_ing)

                productos[prod_data["nombre"]] = prod
            else:
                productos[prod_data["nombre"]] = existing

        session.commit()
        return productos

    # ============ EJECUTAR SEEDS ============
    try:
        print("Seeding ingredientes...")
        ingredientes = seed_ingredientes()
        print(f"{len(ingredientes)} ingredientes seeded")

        print("Seeding categorias...")
        categorias = seed_categorias()
        print(f"{len(categorias)} categorias seeded")

        print("Seeding productos...")
        productos = seed_productos(categorias, ingredientes)
        print(f"{len(productos)} productos seeded")

        print("SEED COMPLETO EXITOSO")
    except Exception as e:
        print(f"Error en seed: {str(e)}")
        session.rollback()
        raise
