import os
from sqlmodel import SQLModel, create_engine, Session

# SQLite Configuration
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///database.db"
)

# JWT Configuration
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "tu-clave-secreta-super-segura-para-desarrollo-local")
JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

engine = create_engine(
    DATABASE_URL,
    echo=False,
    pool_size=10,
    max_overflow=20,
)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
