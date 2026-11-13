"""Tratamento de erros padronizado.

Todo erro da API responde no mesmo formato:
    {"status": 409, "message": "A sala já está reservada nesse horário."}

Erros de validação (422) incluem também a lista de campos:
    {"status": 422, "message": "...", "errors": [{"field": "end", "message": "..."}]}

O FastAPI, por padrão, responde erros de validação em outro formato
({"detail": [...]}), por isso tratamos RequestValidationError aqui.
"""
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException


def _error_response(status: int, message: str, **extra) -> JSONResponse:
    return JSONResponse(status_code=status, content={"status": status, "message": message, **extra})


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request: Request, exc: StarletteHTTPException):
        # Cobre HTTPException(404, 403, 409...) levantadas nas rotas e rotas inexistentes.
        response = _error_response(exc.status_code, str(exc.detail))
        if exc.headers:
            response.headers.update(exc.headers)  # ex.: WWW-Authenticate no 401
        return response

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        errors = [
            {
                # loc é algo como ("body", "end"); o nome do campo é o último item.
                "field": str(err["loc"][-1]),
                "message": err["msg"],
            }
            for err in exc.errors()
        ]
        return _error_response(422, "Erro de validação.", errors=errors)
