import sys
from pathlib import Path

from pydantic import BaseSettings, Field
from loguru import logger


ENVS_PATH = Path("env")

__all__ = [
    "settings",
]


class DB(BaseSettings):
    driver: str
    user: str
    password: str
    host: str
    port: int
    database: str


class Security(BaseSettings):
    access_token_expire_minutes: int
    secret_key: str
    algorithm: str


class API(BaseSettings):
    title: str
    version: str = Path("v1")
    build_version: str
    version_path: Path | None = Path(version)


class Misc(BaseSettings):
    logger_level: str


class Settings(BaseSettings):
    db: DB
    security: Security
    api: API
    misc: Misc


db = DB(_env_file=ENVS_PATH / "db.env")
security = Security(_env_file=ENVS_PATH / "security.env")
api = API(_env_file=ENVS_PATH / "api.env")
misc = Misc(_env_file=ENVS_PATH / "misc.env")

settings = Settings(
    db=db,
    security=security,
    api=api,
    misc=misc
)

if (level := settings.misc.logger_level) != "DEBUG":
    logger.remove()
    logger.add(sys.stderr, level=level)
