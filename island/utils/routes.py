import builtins
from importlib import import_module
from pkgutil import iter_modules
from types import ModuleType

from fastapi import APIRouter
from loguru import logger
from strawberry.fastapi import GraphQLRouter


def get_modules(module: ModuleType, /, *, global_namespace: str):
    """Import all modules and add them to the global namesapce, which can be accessed
    by the key set by `global_namespace`.
    """
    module_path = str(module.__file__)

    if module_path.endswith("__init__.py"):
        module_path = module_path.split("__init__.py")[0]

    if global_namespace is not None:
        if not hasattr(builtins, global_namespace):
            setattr(builtins, global_namespace, [])

    for a, module_name, is_pkg in iter_modules([module_path]):
        m_name = f"{module.__name__}.{module_name}"
        prefix = ""

        logger.debug(f"Importing module: {m_name}")
        module_imp = import_module(m_name, package=module_path)

        if is_pkg:
            get_modules(module_imp, global_namespace=global_namespace)
            continue

        if global_namespace is not None:
            getattr(builtins, global_namespace).append(module_imp)


def get_graphql_routers(module: ModuleType) -> APIRouter:
    """dynamically import all routers under `graphql` under a common `APIRouter`.
    The directory & folder structural naming will be used as prefix.

    Args:
        module (module, optional): _description_. Defaults to None.

    Returns:
        GraphQLRouter: GraphQL router
    """

    _prefix = f"{('/' + module.__name__.split('.')[-1]) if module else ''}"
    module_path = str(module.__file__)

    if module_path.endswith("__init__.py"):
        module_path = module_path.split("__init__.py")[0]

    route = (
        APIRouter(prefix=f"/{module.__prefix__.strip('/')}")
        if hasattr(module, "__prefix__")
        else APIRouter(prefix=_prefix)
    )

    for a, module_name, is_pkg in iter_modules([module_path]):
        m_name = f"{module.__name__}.{module_name}"
        prefix = ""

        logger.debug(f"Importing router module: {m_name}")
        module_imp = import_module(m_name, package=module_path)

        if hasattr(module_imp, "__skip__"):
            logger.debug(
                f"Skipping import GraphQL from module: {m_name}. Reason: __skip__ is set to True"
            )
            continue

        if is_pkg:
            logger.warning(
                f"Skipping import GraphQL from module: {m_name}. Reason: it is not a package"
            )
            continue

        if not hasattr(module_imp, "schema"):
            logger.warning(
                f"Skipping import GraphQL from module: {m_name}. Reason: it doesn't have a schema"
            )
            continue

        if hasattr(module_imp, "__prefix__"):
            prefix += f"/{module_imp.__prefix__}"
        else:
            prefix += f"/{module_name}"

        logger.info(f"Including router: {prefix}")

        try:
            router = GraphQLRouter(module_imp.schema)
            route.include_router(router, prefix=prefix)
        except Exception as e:
            logger.warning(
                f"Skipping import GraphQL from module: {m_name}. Reason: Error when trying to create router for schema"
            )

    return route
