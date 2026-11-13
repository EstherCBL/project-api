"""Configurações da aplicação.

Os valores vêm de variáveis de ambiente (ou do arquivo .env).
Assim a chave secreta e a URL do banco não ficam fixas no código.
"""
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./reservas.db"
    SECRET_KEY: str = "dev-only-troque-em-producao"
    ALGORITHM: str = "HS256"
    # Expiração curta: não existe logout, o token só deixa de valer ao expirar.
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
