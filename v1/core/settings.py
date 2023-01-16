from pathlib import Path

from pydantic import BaseSettings, Field

ENVS_PATH = Path("env")

__all__ = [
    "settings"
]


# noinspection PyUnboundLocalVariable
class _DBSettings(BaseSettings):
    driver: str
    user: str
    password: str
    host: str
    port: int
    database: str


class _SecuritySettings(BaseSettings):
    access_token_expire_minutes: int
    secret_key: str
    algorithm: str


# noinspection PyUnboundLocalVariable
class _APISettings(BaseSettings):
    title: str
    version: str = Path("v1")
    build_version: str
    version_path: Path | None = Path(version)


class _Settings(BaseSettings):
    db: _DBSettings
    security: _SecuritySettings
    api: _APISettings


_db_settings = _DBSettings(_env_file=ENVS_PATH / "db.env")
_security_settings = _SecuritySettings(_env_file=ENVS_PATH / "security.env")
_api_settings = _APISettings(_env_file=ENVS_PATH / "api.env")

settings = _Settings(
    db=_db_settings,
    security=_security_settings,
    api=_api_settings
)
