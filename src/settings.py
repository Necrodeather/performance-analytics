from functools import lru_cache
from typing import Optional

from pydantic import BaseSettings, Field, PostgresDsn, validator


class Settings(BaseSettings):
    DEBUG: bool = Field(default=False)
    SERVER_HOST: str = Field(default="localhost")
    SERVER_PORT: int = Field(default=8000)
    POSTGRES_SCHEME: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str = Field(default="localhost")
    POSTGRES_PORT: str = Field(default="5432")
    POSTGRES_DB: str
    DATABASE_URI: Optional[PostgresDsn]

    @validator("DATABASE_URI")
    def generate_dsn(cls, value: str, values: dict) -> str:
        if isinstance(value, str):
            return value
        return PostgresDsn.build(
            scheme=values.get("POSTGRES_SCHEME"),
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_HOST"),
            port=values.get("POSTGRES_PORT"),
            path=f'/{values.get("POSTGRES_DB") or "postgres"}',
        )

    class Config:
        env_file = ".env"


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
