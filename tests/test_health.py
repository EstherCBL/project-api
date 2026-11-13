def test_health_retorna_ok(client):
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_rota_inexistente_usa_formato_de_erro_padrao(client):
    response = client.get("/api/nao-existe")
    assert response.status_code == 404
    body = response.json()
    assert body["status"] == 404
    assert "message" in body
