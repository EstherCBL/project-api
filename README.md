# API de Reserva de Salas

API REST para reserva de salas e laboratórios por horário.
Stack: **Python + FastAPI**, SQLAlchemy, Alembic, Pydantic, bcrypt, PyJWT, pytest.

## Como rodar

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env             # Windows: copy .env.example .env
uvicorn app.main:app --reload
```

- API: http://127.0.0.1:8000/api/health
- Documentação interativa (Swagger): http://127.0.0.1:8000/docs

## Testes

```bash
pytest
```

Os testes usam um banco SQLite em memória, separado do banco real.

## Migrations (Alembic)

```bash
alembic revision --autogenerate -m "descricao"   # gera a migration a partir dos models
alembic upgrade head                              # aplica no banco
```

## Estrutura

```
app/
  main.py          # cria o app, registra handlers de erro e rotas
  database.py      # engine, sessão, Base e get_db
  core/
    config.py      # configurações (.env)
    errors.py      # formato padrão de erro { status, message, errors? }
  models/          # tabelas (SQLAlchemy)
  schemas/         # entrada e saída (Pydantic)
  routers/         # rotas
alembic/           # migrations
tests/             # testes (pytest + TestClient)
```

## Formato de erro

```json
{ "status": 409, "message": "A sala já está reservada nesse horário." }
```

Erros de validação (422) incluem `"errors": [{ "field": "end", "message": "..." }]`.

## Status

- [x] Semana 15: estrutura inicial, configuração, banco e Alembic
- [ ] Semana 16: models, migrations, CRUD de salas, seed do admin
- [ ] Semana 17: usuários, login e JWT
- [ ] Semana 18: reservas e regra de conflito
- [ ] Semana 19: testes, README final e exemplos de requisições
