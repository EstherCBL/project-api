from app.core.security import hash_password, verify_password
from app.models.user import User

USUARIO = {"name": "Maria", "email": "maria@teste.com", "password": "senha123"}


def test_hash_nao_guarda_a_senha():
    h = hash_password("senha123")
    assert h != "senha123"
    assert h.startswith("$2b$")
    assert verify_password("senha123", h)
    assert not verify_password("errada", h)


def test_mesma_senha_gera_hash_diferente():
    assert hash_password("senha123") != hash_password("senha123")


def test_cadastro_grava_hash_e_nao_devolve(client, Session):
    r = client.post("/api/register", json=USUARIO)
    assert r.status_code == 201
    body = r.json()
    assert "password" not in body
    assert "password_hash" not in body

    with Session() as db:
        user = db.query(User).filter(User.email == USUARIO["email"]).one()
        assert user.password_hash != USUARIO["password"]
        assert verify_password(USUARIO["password"], user.password_hash)


def test_login_com_senha_errada(client):
    client.post("/api/register", json=USUARIO)
    r = client.post("/api/login", json={"email": USUARIO["email"], "password": "errada"})
    assert r.status_code == 401

    r = client.post("/api/login", json={"email": USUARIO["email"], "password": USUARIO["password"]})
    assert r.status_code == 200
    assert "access_token" in r.json()


def test_senha_maior_que_72_bytes(client):
    r = client.post("/api/register", json={**USUARIO, "password": "a" * 80})
    assert r.status_code == 422
    assert r.json()["errors"][0]["field"] == "password"
