import importlib
import os

import uvicorn as uvicorn
from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

from v1.core.settings import settings

DB_URL_FMT = "{driver}://{user}:{password}@{host}:{port}/{database}"

application = FastAPI(
    title=settings.api.title,
    version=f"{settings.api.version}.{settings.api.build_version}"
)


def configure_tortoise(app: FastAPI):
    """
    Generates a list of paths to the models, includes aerich, then registers Tortoise

    :param app: Instance of FastAPI class
    :return:
    """
    db = settings.db
    models = [
        f'v1.applications.{model_dir}.models'
        for model_dir in os.listdir(settings.api.version_path / "applications")
    ]
    models.append("aerich.models")

    register_tortoise(
        app,
        db_url=DB_URL_FMT.format(
            driver=db.driver,
            user=db.user,
            password=db.password,
            host=db.host,
            port=db.port,
            database=db.database
        ),
        modules={
            'models': models
        },
        generate_schemas=True,
        add_exception_handlers=True,
    )


def include_routers(app: FastAPI):
    """
    Routers must contain the variables **__tags__** and **__prefix__** \n
    If router's name starts with "_" it won't be included

    :param app: Instance of FastAPI class
    :return: None
    """
    for module_name in os.listdir(settings.api.version_path / "routers"):
        if module_name.startswith("_") or not module_name.endswith(".py"):
            continue

        module = importlib.import_module(f"v1.routers.{module_name.removesuffix('.py')}")

        app.include_router(
            module.router, tags=module.__tags__, prefix=module.__prefix__
        )


configure_tortoise(application)
include_routers(application)


if __name__ == "__main__":
    uvicorn.run("main:application", reload=True)
