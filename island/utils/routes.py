import builtins
from importlib import import_module
from pkgutil import iter_modules
from types import ModuleType

from loguru import logger


def get_modules(module: ModuleType, /, *, global_namespace: str):
    """Import all modules and add them to the global namespace, which can be accessed
    by the key set by `global_namespace`.
    """
    module_path = str(module.__file__)

    if module_path.endswith("__init__.py"):
        module_path = module_path.split("__init__.py")[0]

    if global_namespace is not None and not hasattr(builtins, global_namespace):
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
