from typing import Any, Callable
from fastapi import FastAPI

from dependencies.registrator import dependencies_container
from core.config import logger


def setup_dependencies(app: FastAPI, mapper: dict[Any, Callable] | None = None) -> None:
    if mapper is None:
        mapper = dependencies_container
    for interface, dependency in mapper.items():
        app.dependency_overrides[interface] = dependency
    
    return dependencies_container
