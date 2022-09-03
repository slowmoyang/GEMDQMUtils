import os
from dataclasses import dataclass
from typing import Optional
import getpass
import signal
from functools import cache
from omsapi import OMSAPI

PASSWORD_PROMPT_TIMEOUT = int(os.getenv("GEM_DMQ_PASSWORD_PROMPT_TIMEOUT", 30)) # sec
MAX_PER_PAGE = 100000

@dataclass
class ClientAuth:
    id: str
    secret: str

def get_client_auth_from_prompt():
    client_id = getpass.getpass(prompt='OMS API Client ID: ')
    signal.signal(signal.SIGALRM, lambda *_: TimeoutError())
    signal.alarm(PASSWORD_PROMPT_TIMEOUT)
    client_secret = getpass.getpass(
            prompt=f'OMS API Client Secret (timeout after {PASSWORD_PROMPT_TIMEOUT} sec): ')
    signal.alarm(0)
    return ClientAuth(client_id, client_secret)

# TODO check if it is vulnerable to pass a secret through env var
def get_client_auth_from_env() -> Optional[ClientAuth]:
    client_id = os.getenv('GEM_DQM_OMS_API_CLIENT_ID')
    client_secret = os.getenv('GEM_DQM_OMS_API_CLIENT_SECRET')
    if client_id is not None and client_secret is not None:
        return ClientAuth(client_id, client_secret)

@cache
def load_oms_api(api_url: str = "https://cmsoms.cern.ch/agg/api",
                 api_version: str = 'v1'
) -> OMSAPI:
    omsapi = OMSAPI(api_url, api_version, cert_verify=False)
    auth = get_client_auth_from_env() or get_client_auth_from_prompt()
    omsapi.auth_oidc(client_id=auth.id, client_secret=auth.secret)
    return omsapi
