import pkgutil
import inspect
import importlib
from characters.creature import Creature  # Your base class

ALL_CREATURES = []

# Dynamically import all modules in this package
for module_info in pkgutil.iter_modules(__path__):
    module = importlib.import_module(f"{__name__}.{module_info.name}")

    # Find classes in the module that are subclasses of Creature
    for name, obj in inspect.getmembers(module, inspect.isclass):
        if issubclass(obj, Creature) and obj is not Creature:
            # Ensure the class is defined in this module (avoid duplicates)
            if obj.__module__ == module.__name__:
                ALL_CREATURES.append(obj)

# For convenience
CREATURES_BY_NAME = {cls.__name__: cls for cls in ALL_CREATURES}