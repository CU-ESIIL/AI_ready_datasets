"""Content-addressed immutable JSON artifacts shared safely between tracks."""
import json
from pathlib import Path
from .contracts import digest


def cached(root: Path, identity, producer):
    """Read-through cache with content integrity and exclusive atomic publication."""
    import os
    import tempfile
    key = digest(identity)
    path = Path(root) / "index" / f"{key}.json"
    def read():
        saved = json.loads(path.read_text())
        if saved["identity"] != identity or saved["digest"] != digest(saved["value"]):
            raise ValueError("immutable cache entry corrupted")
        return saved["value"], key
    if path.exists():
        return read()
    value = producer()
    payload = {"identity": identity, "value": value, "digest": digest(value)}
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(mode="w", dir=path.parent, delete=False) as handle:
            temporary = Path(handle.name)
            json.dump(payload, handle, sort_keys=True, indent=2, allow_nan=False)
            handle.write("\n")
        try:
            os.link(temporary, path)
        except FileExistsError:
            pass
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)
    return read()
