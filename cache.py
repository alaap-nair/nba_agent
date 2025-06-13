"""Simple disk and memory cache utilities."""
import json
import hashlib
from pathlib import Path

CACHE_DIR = Path("cache")
CACHE_DIR.mkdir(exist_ok=True)

_memory_cache = {}

__all__ = ["get", "set", "_path_for_key"]

def _path_for_key(key: str) -> Path:
    hashed = hashlib.md5(key.encode()).hexdigest()
    return CACHE_DIR / f"{hashed}.json"

def get(key: str):
    if key in _memory_cache:
        return _memory_cache[key]
    path = _path_for_key(key)
    if path.exists():
        data = json.loads(path.read_text())
        _memory_cache[key] = data
        return data
    return None

def set(key: str, data) -> None:
    path = _path_for_key(key)
    path.write_text(json.dumps(data))
    _memory_cache[key] = data
