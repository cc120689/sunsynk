import logging
import os
import sys
from importlib import import_module as _import_module
from pathlib import Path
from types import ModuleType
from typing import Optional

_LOGGER = logging.getLogger(__name__)


def import_module(mod_name, folder: str) -> ModuleType:
    """import_module."""
    here = Path(os.getcwd()) / folder
    sys.path.insert(0, str(here))
    try:
        mod_obj = _import_module(mod_name)
        return mod_obj
    finally:
        sys.path.pop(0)


def import_mysensors() -> Optional[dict[str, any]]:
    """Import my sensors."""
    root = "/share/hass-addon-sunsynk/"
    modn = "mysensors"
    pth = Path(root) / f"{modn}.py"
    if not pth.exists():
        return None
    _LOGGER.info("Importing %s...", pth)
    mod = import_module("mysensors", root)
    sensors = getattr(mod, "SENSORS", None)
    if not sensors:
        _LOGGER.error("No SENSORS variable found in mysensors.py")
        return None
    all: dict[str, any] = getattr(sensors, "all", {})
    if all:
        _LOGGER.info("  custom sensors: %s", ", ".join(all))
    else:
        _LOGGER.warning("  no custom sensors")
    return all
