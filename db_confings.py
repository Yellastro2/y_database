import os
from threading import RLock


default_name = None
_active_name = None
_config_lock = RLock()


def configure(f_name):
  """Configure the default database before its first actual use."""
  global default_name

  f_name = os.fspath(f_name)
  if not f_name:
    raise ValueError("Database name must not be empty")

  with _config_lock:
    if _active_name is not None and f_name != _active_name:
      raise RuntimeError(
        f"Database is already in use as {_active_name!r}; "
        f"cannot switch it to {f_name!r}"
      )
    default_name = f_name


def get_default_name():
  """Return and lock the configured database name on first use."""
  global _active_name

  with _config_lock:
    if default_name is None:
      raise RuntimeError(
        "y_database is not configured. "
        "Call y_database.configure('database.db') before the first query"
      )
    _active_name = default_name
    return default_name


def set_default_name(f_name):
  """Backward-compatible alias for configure()."""
  configure(f_name)
