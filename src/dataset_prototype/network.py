"""Bounded HTTP transport; no credential values in persisted request evidence."""
import json
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError


class AccessError(ValueError):
    pass


def request_bytes(url, *, payload=None, headers=None, timeout=60, max_bytes=8_000_000):
    body = json.dumps(payload, allow_nan=False).encode() if payload is not None else None
    request = Request(url, data=body, headers={"User-Agent": "dataset-prototype/0.1", **({"Content-Type": "application/json"} if body else {}), **(headers or {})})
    try:
        with urlopen(request, timeout=timeout) as response:
            content = response.read(max_bytes + 1)
    except HTTPError as error:
        raise AccessError(f"HTTP {error.code} from requested service; verify access/token (no fallback to fixtures)") from None
    except (URLError, TimeoutError) as error:
        raise AccessError(f"Requested service unavailable: {type(error).__name__}") from None
    if len(content) > max_bytes:
        raise AccessError("response exceeds configured byte limit")
    return content


def request_json(url, **kwargs):
    return json.loads(request_bytes(url, **kwargs))
