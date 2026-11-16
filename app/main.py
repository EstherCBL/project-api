from fastapi import FastAPI

from app.core.errors import register_exception_handlers
from app.routers import health

app = FastAPI(title="Reserva de Salas")

register_exception_handlers(app)
app.include_router(health.router, prefix="/api")
