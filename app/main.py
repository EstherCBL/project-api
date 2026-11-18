from fastapi import FastAPI

from app.core.errors import register_exception_handlers
from app.routers import health, rooms

app = FastAPI(title="Reserva de Salas")

register_exception_handlers(app)
app.include_router(health.router, prefix="/api")
app.include_router(rooms.router, prefix="/api")