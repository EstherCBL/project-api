# API de Reserva de Salas

API para reservar salas e laboratórios por horário. Feita com FastAPI + SQLAlchemy.

## Rodando

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
uvicorn app.main:app --reload
```

Depois é só abrir http://127.0.0.1:8000/docs

## Testes

```bash
pytest
```

## Migrations

```bash
alembic revision --autogenerate -m "mensagem"
alembic upgrade head
```

## TODO

- models e CRUD de salas
- usuários, login com JWT
- reservas (não deixar reservar horário que já está ocupado)
