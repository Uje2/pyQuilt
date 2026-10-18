import importlib

_registry = {}
_cache = {}

def register(name, path):
    """path format: 'package.module:ClassName'"""
    _registry[name] = path

def resolve(name):
    if name in _cache:
        return _cache[name]
    if name not in _registry:
        raise KeyError(f"Unknown registered type: {name!r}")
    mod_path, cls_name = _registry[name].split(":")
    obj = getattr(importlib.import_module(mod_path), cls_name)
    _cache[name] = obj
    return obj

def create(name, *args, **kwargs):
    return resolve(name)(*args, **kwargs)

def registered():
    return sorted(_registry)

# backwards-compat alias so widgets.py keeps working with register_type(...)
register_type = register