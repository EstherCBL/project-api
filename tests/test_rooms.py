SALA = {"name": "Lab 1", "capacity": 30, "location": "Bloco A"}


def criar_sala(client, **dados):
    r = client.post("/api/rooms", json={**SALA, **dados})
    assert r.status_code == 201
    return r.json()


def test_criar_sala(client):
    r = client.post("/api/rooms", json=SALA)
    assert r.status_code == 201
    body = r.json()
    assert body["id"] > 0
    assert body["name"] == "Lab 1"
    assert body["capacity"] == 30
    assert body["location"] == "Bloco A"


def test_listar_salas(client):
    criar_sala(client)
    criar_sala(client, name="Sala 201")
    r = client.get("/api/rooms")
    assert r.status_code == 200
    body = r.json()
    assert len(body["items"]) == 2
    assert body["total"] == 2
    assert body["page"] == 1


def test_editar_capacidade(client):
    sala = criar_sala(client)
    r = client.put(f"/api/rooms/{sala['id']}", json={**SALA, "capacity": 50})
    assert r.status_code == 200
    assert r.json()["capacity"] == 50


def test_apagar_sala(client):
    sala = criar_sala(client)
    r = client.delete(f"/api/rooms/{sala['id']}")
    assert r.status_code == 204
    r = client.get("/api/rooms")
    ids = [s["id"] for s in r.json()["items"]]
    assert sala["id"] not in ids


def test_editar_sala_inexistente(client):
    r = client.put("/api/rooms/999", json=SALA)
    assert r.status_code == 404
    assert r.json() == {"status": 404, "message": "Sala não encontrada."}


def test_apagar_sala_inexistente(client):
    r = client.delete("/api/rooms/999")
    assert r.status_code == 404
    assert r.json() == {"status": 404, "message": "Sala não encontrada."}


def test_capacidade_zero(client):
    r = client.post("/api/rooms", json={**SALA, "capacity": 0})
    assert r.status_code == 422
    fields = [e["field"] for e in r.json()["errors"]]
    assert "capacity" in fields
