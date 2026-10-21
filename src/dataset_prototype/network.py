"""Bounded HTTP transport; no credential values in persisted request evidence."""
import json
from urllib.request import Request, urlopen, HTTPRedirectHandler, build_opener
from urllib.parse import urlsplit
from urllib.error import HTTPError, URLError


class AccessError(ValueError):
    pass


class CredentialRedirectGuard(HTTPRedirectHandler):
    def redirect_request(self, request, fp, code, message, headers, newurl):
        credentials = any(name.lower() in {"authorization", "x-api-token"} for name, _ in request.header_items())
        origin = lambda url: (urlsplit(url).scheme, urlsplit(url).hostname, urlsplit(url).port)
        if credentials and origin(request.full_url) != origin(newurl):
            raise AccessError("credential-bearing redirect to another origin refused")
        return super().redirect_request(request, fp, code, message, headers, newurl)


def request_bytes(url, *, payload=None, headers=None, timeout=60, max_bytes=8_000_000):
    body = json.dumps(payload, allow_nan=False).encode() if payload is not None else None
    request = Request(url, data=body, headers={"User-Agent": "dataset-prototype/0.1", **({"Content-Type": "application/json"} if body else {}), **(headers or {})})
    try:
        with build_opener(CredentialRedirectGuard()).open(request, timeout=timeout) as response:
            content = response.read(max_bytes + 1)
    except HTTPError as error:
        detail = "verify access/token" if error.code in {401, 403} else "service rejected the request or failed"
        raise AccessError(f"HTTP {error.code} from requested service; {detail} (no fallback to fixtures)") from None
    except (URLError, TimeoutError) as error:
        raise AccessError(f"Requested service unavailable: {type(error).__name__}") from None
    if len(content) > max_bytes:
        raise AccessError("response exceeds configured byte limit")
    return content


def request_json(url, **kwargs):
    return json.loads(request_bytes(url, **kwargs))
