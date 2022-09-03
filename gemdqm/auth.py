import os
from dataclasses import dataclass
from functools import cache
from typing import Optional
from pathlib import Path
import http.client
from http import HTTPStatus
import urllib.request
import ssl

CERN_CERTIFICATE = "GEM_DQM_CERN_CERTIFICATE"

@dataclass
class CertChain:
    certfile: str
    keyfile: str

@cache
def load_cert_chain() -> CertChain:
    if (cert_dir := os.getenv(CERN_CERTIFICATE)) is not None:
        cert_dir = Path(cert_dir)
    else:
        cert_dir = Path.home() / '.globus'
        print(f"The environment variable '{CERN_CERTIFICATE}' is not set. It fallbacks to '{str(cert_dir)}'")

    if not cert_dir.exists():
        raise FileNotFoundError(cert_dir)

    certfile = cert_dir / 'usercert.pem'
    if not certfile.exists():
        raise FileNotFoundError(certfile)

    keyfile = cert_dir / 'userkey.pem'
    if not keyfile.exists():
        raise FileNotFoundError(keyfile)

    return CertChain(str(certfile), str(keyfile))


class HTTPSAuthConnection(http.client.HTTPSConnection):
    def __init__(self,
                 host: str,
                 context: Optional[ssl.SSLContext] = None,
                 **kwargs
    ) -> None:
        context = context or ssl._create_default_https_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE

        cert_chain = load_cert_chain()
        context.load_cert_chain(certfile=cert_chain.certfile,
                                keyfile=cert_chain.keyfile,
                                password=None)

        super().__init__(host, context=context, **kwargs)


class HTTPSAuthHandler(urllib.request.AbstractHTTPHandler):
    def default_open(self, req):
        return self.do_open(http_class=HTTPSAuthConnection, # type: ignore
                            req=req)

def open_url(url):
    response = urllib.request.build_opener(HTTPSAuthHandler()).open(url)
    if response.status != HTTPStatus.OK:
        raise RuntimeError(f'[{response.status=}] {url=:s}')
    return response
