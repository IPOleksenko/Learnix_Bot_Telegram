import os
import importlib

def import_submodules(package_name, package_path):
    for entry in os.scandir(package_path):
        if entry.is_file() and entry.name.endswith(".py") and entry.name != "__init__.py":
            module = f"{package_name}.{entry.name[:-3]}"
            importlib.import_module(module)

        elif entry.is_dir():
            subpackage = f"{package_name}.{entry.name}"
            subpath = entry.path
            importlib.import_module(subpackage)
            import_submodules(subpackage, subpath)

import_submodules(__name__, os.path.dirname(__file__))
