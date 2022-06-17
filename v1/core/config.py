from pathlib import Path
from typing import Optional

from pydantic.env_settings import BaseSettings


class DatabaseSettings(BaseSettings):
    name: str
    ip_address: str
    port: int
    user: str = "postgres"
    password: str = "postgres"


class SecuritySettings(BaseSettings):
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    SECRET_KEY: str
    ALGORITHM: str


class ServerSettings(BaseSettings):
    version: str
    csrf_token: str
    db_settings: Optional[DatabaseSettings]
    security_settings: Optional[SecuritySettings]


API_VER = Path("v1")
ENVS = API_VER / "envs"

server_env_file = ENVS / "server.env"
db_env_file = ENVS / "db.env"
security_env_file = ENVS / "security.env"

settings = ServerSettings(_env_file=server_env_file, _env_file_encoding="utf-8")
settings.db_settings = DatabaseSettings(_env_file=db_env_file, _env_file_encoding="utf-8")
settings.security_settings = SecuritySettings(_env_file=security_env_file, _env_file_encoding="utf-8")
