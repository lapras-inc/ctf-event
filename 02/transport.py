"""Map the public partner origin onto the isolated fixture transport."""
import os
from urllib.parse import urlsplit

from requests.adapters import HTTPAdapter
from requests.exceptions import InvalidURL


class FixtureOnlyAdapter(HTTPAdapter):
    def send(self, request, **kwargs):
        url = urlsplit(request.url)
        port = os.environ.get("PARTNER_PORT", "8012")
        if url.scheme == "http" and url.netloc in {f"localhost:{port}", f"127.0.0.1:{port}"}:
            request = request.copy()
            request.url = url._replace(netloc="partner:8000").geturl()
            url = urlsplit(request.url)
        routes = {
            "partner:8000": {"/", "/article", "/go"},
            "vault:8000": {"/document"},
        }
        if (url.scheme != "http" or url.netloc not in routes
                or url.path not in routes[url.netloc]
                or url.username or url.password or url.fragment):
            raise InvalidURL("Outside the challenge fixtures")
        return super().send(request, **kwargs)
