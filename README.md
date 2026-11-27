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

No `.env`, troque o `SECRET_KEY` por uma chave grande. Dá pra gerar uma com:

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

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

O email e a senha do admin vêm de `ADMIN_EMAIL` e `ADMIN_PASSWORD` no `.env`. Rodar de novo não duplica nada.

## TODO

- reservas (não deixar reservar horário que já está ocupado)
- cancelamento de reserva só pelo dono ou admin
