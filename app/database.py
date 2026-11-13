"""Conexão com o banco via SQLAlchemy.

- engine: a "conexão" com o banco.
- SessionLocal: fábrica de sessões (uma sessão por requisição).
- Base: classe-mãe de todos os models (o Alembic lê os models a partir dela).
- get_db: dependência do FastAPI que abre e fecha a sessão.
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.core.config import settings

# SQLite precisa desse argumento para ser usado em várias threads (uvicorn).
connect_args = (
    {"check_same_thread": False} if settings.DATABASE_URL.startswith("sqlite") else {}
)

engine = create_engine(settings.DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


class Base(DeclarativeBase):
    pass


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
