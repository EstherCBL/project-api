from fastapi import APIRouter

router = APIRouter(tags=["health"])


@router.get("/health")
def health():
    """Rota simples para confirmar que a API está no ar."""
    return {"status": "ok"}
