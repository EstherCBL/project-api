from app.core.security import create_access_token, decode_access_token

SALA = {"name": "Lab 1", "capacity": 30, "location": "Bloco A"}
ANA = {"name": "Ana", "email": "ana@teste.com", "password": "senha123"}


def test_token_guarda_id_e_role():
    payload = decode_access_token(create_access_token({"sub": "42", "role": "user"}))
    assert payload["sub"] == "42"
    assert payload["role"] == "user"
    assert "exp" in payload


def test_sem_token_retorna_401(client):
    r = client.post("/api/rooms", json=SALA)
    assert r.status_code == 401
    assert r.json()["message"] == "Faça login para acessar esta rota."


def test_token_invalido_retorna_401(client):
    r = client.post("/api/rooms", json=SALA, headers={"Authorization": "Bearer token-invalido"})
    assert r.status_code == 401
    assert r.json()["message"] == "Token inválido ou expirado."


def test_usuario_comum_retorna_403(client):
    client.post("/api/register", json=ANA)
    token = client.post("/api/login", json={"email": ANA["email"], "password": ANA["password"]}).json()["access_token"]
    r = client.post("/api/rooms", json=SALA, headers={"Authorization": f"Bearer {token}"})
    assert r.status_code == 403


def test_login_pelo_formulario_do_docs(client):
    client.post("/api/register", json=ANA)
    r = client.post("/api/token", data={"username": ANA["email"], "password": ANA["password"]})
    assert r.status_code == 200
    assert "access_token" in r.json()
