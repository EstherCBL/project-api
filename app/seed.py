import app.models  # noqa: F401
from app.core.config import settings
from app.core.security import hash_password
from app.database import SessionLocal
from app.models.room import Room
from app.models.user import User

SALAS_EXEMPLO = [
    {"name": "Lab 1", "capacity": 30, "location": "Bloco A"},
    {"name": "Sala 201", "capacity": 40, "location": "Bloco B, 2º andar"},
    {"name": "Auditório", "capacity": 150, "location": "Bloco C"},
]


def seed(db):
    admin = db.query(User).filter(User.email == settings.ADMIN_EMAIL).first()
    if not admin:
        db.add(User(
            name="Admin",
            email=settings.ADMIN_EMAIL,
            password_hash=hash_password(settings.ADMIN_PASSWORD),
            role="admin",
        ))
        print(f"Admin criado: {settings.ADMIN_EMAIL}")
    else:
        print("Admin já existe.")

    if db.query(Room).count() == 0:
        for sala in SALAS_EXEMPLO:
            db.add(Room(**sala))
        print(f"{len(SALAS_EXEMPLO)} salas de exemplo criadas.")
    else:
        print("Já existem salas cadastradas.")

    db.commit()


if __name__ == "__main__":
    db = SessionLocal()
    try:
        seed(db)
    finally:
        db.close()
