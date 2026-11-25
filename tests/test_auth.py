from fastapi import Depends
from fastapi.testclient import TestClient

from app.core.deps import get_current_user, require_admin
from app.core.security import create_access_token, decode_access_token
from app.main import app


@app.get("/_test/protected-user")
def _protected_user_route(user=Depends(get_current_user)):
    return {"user_id": user.id, "role": user.role}


@app.get("/_test/protected-admin")
def _protected_admin_route(admin=Depends(require_admin)):
    return {"admin_id": admin.id, "role": admin.role}


def test_create_and_decode_token():
    token = create_access_token(data={"sub": "42", "role": "user"})
    payload = decode_access_token(token)
    assert payload["sub"] == "42"
    assert payload["role"] == "user"
    assert "exp" in payload


def test_protected_route_without_token_returns_401():
    client = TestClient(app)
    response = client.get("/_test/protected-user")
    assert response.status_code == 401


def test_protected_route_with_invalid_token_returns_401():
    client = TestClient(app)
    response = client.get(
        "/_test/protected-user",
        headers={"Authorization": "Bearer token-invalido"},
    )
    assert response.status_code == 401