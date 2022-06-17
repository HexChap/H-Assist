import importlib
import os
from pathlib import Path

import uvicorn
from fastapi.applications import FastAPI
from tortoise.contrib.fastapi import register_tortoise

from v1.core.config import settings

db_settings = settings.db_settings
DB_URL = f"postgres://{db_settings.user}:{db_settings.password}@{db_settings.ip_address}:{db_settings.port}/{db_settings.name}"
PATH_TO_V1 = Path("v1")

app = FastAPI(title="H-Assist")


def include_routers(app: FastAPI):
    for module_name in os.listdir(PATH_TO_V1 / "routers"):
        if module_name.startswith("_") or not module_name.endswith(".py"):
            continue

        module = importlib.import_module(f"v1.routers.{module_name.removesuffix('.py')}")

        app.include_router(
            module.router, tags=module.__tags__, prefix=module.__prefix__
        )


def get_model_paths():
    app_list = [f'v1.applications.{model_dir}.models' for model_dir in os.listdir(PATH_TO_V1 / "applications")]
    app_list.append('aerich.models')

    return app_list


def get_tortoise_config() -> dict:
    model_paths = get_model_paths()
    DB_CONNECTIONS = {
        'default': {
            'engine': 'tortoise.backends.asyncpg',
            'db_url': DB_URL,
            'credentials': {
                'host': f'{db_settings.ip_address}',
                'port': f'{db_settings.port}',
                'user': f'{db_settings.user}',
                'password': f'{db_settings.password}',
                'database': f'{db_settings.name}',
            }
        },
    }

    config = {
        'connections': DB_CONNECTIONS,
        'apps': {
            'models': {
                'models': model_paths,
                'default_connection': 'default',
            }
        }
    }
    return config


TORTOISE_ORM = get_tortoise_config()


def register_db(app: FastAPI, db_url: str = DB_URL):
    model_paths = get_model_paths()
    register_tortoise(
        app,
        db_url=db_url,
        modules={'models': model_paths},
        generate_schemas=True,
        add_exception_handlers=True,
    )

# @app.on_event("startup")
# async def startup():
#     await database.connect()
#
#
# @app.on_event("shutdown")
# async def shutdown():
#     await database.disconnect()

register_db(app)
include_routers(app)


if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, host="127.0.0.1", reload=True)


