from fastapi import FastAPI

from app.core.errors import register_exception_handlers
from app.routers import health

app = FastAPI(title="API de Reserva de Salas", version="0.1.0")

register_exception_handlers(app)

# Todas as rotas ficam sob o prefixo /api
app.include_router(health.router, prefix="/api")
