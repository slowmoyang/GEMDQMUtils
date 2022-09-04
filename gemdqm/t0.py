#!/usr/bin/env python
import requests
from bs4 import BeautifulSoup
from http import HTTPStatus
import json

def get_t0_config(run: int, express: bool):
    reco_type = "express" if express else "reco"
    url = f'https://cmsweb.cern.ch/t0wmadatasvc/prod/{reco_type}_config?run={run}'
    response = requests.get(url, verify=False)
    if response.status_code != HTTPStatus.OK:
        raise RuntimeError(f'[{response.status_code=}] {url=:s}')
    soup = BeautifulSoup(response.text, features="html.parser")
    config = json.loads(soup.contents[0]) # type: ignore
    return config
