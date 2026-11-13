"""Importe aqui todos os models (User, Room, Reservation) quando forem criados.

O Alembic só enxerga as tabelas dos models que foram importados.
"""
from app.database import Base  # noqa: F401
