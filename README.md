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

## Admin inicial

Depois de rodar as migrations, crie o admin e as salas de exemplo:

```bash
python -m app.seed
```

O email e a senha do admin vêm de `ADMIN_EMAIL` e `ADMIN_PASSWORD` no `.env`. Pode rodar mais de uma vez: se o admin ou as salas já existirem, nada é duplicado.

## TODO

- models e CRUD de salas
- usuários, login com JWT
- reservas (não deixar reservar horário que já está ocupado)
