def test_health(client):
    r = client.get("/api/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}


def test_404(client):
    r = client.get("/api/nao-existe")
    assert r.status_code == 404
    assert r.json()["status"] == 404
