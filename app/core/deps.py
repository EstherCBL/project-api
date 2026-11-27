import jwt
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.security import decode_access_token
from app.database import get_db
from app.models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/token", auto_error=False)


def get_current_user(token: str | None = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    headers = {"WWW-Authenticate": "Bearer"}
    if not token:
        raise HTTPException(401, "Faça login para acessar esta rota.", headers=headers)

    try:
        user_id = int(decode_access_token(token)["sub"])
    except (jwt.PyJWTError, KeyError, ValueError):
        raise HTTPException(401, "Token inválido ou expirado.", headers=headers)

    user = db.get(User, user_id)
    if not user:
        raise HTTPException(401, "Token inválido ou expirado.", headers=headers)
    return user


def require_admin(user: User = Depends(get_current_user)) -> User:
    if user.role != "admin":
        raise HTTPException(403, "Acesso restrito a administradores.")
    return user
