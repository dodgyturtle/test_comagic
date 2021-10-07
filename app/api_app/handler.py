import json
import re
import typing as t

import requests
from bs4 import BeautifulSoup
from flask import current_app

JSONType = t.Union[str, int, float, bool, None, t.Dict[str, t.Any], t.List[t.Any]]


def post_response(url: str, data: JSONType = None) -> requests.models.Response:
    response = requests.post(url, data=data, verify=False, allow_redirects=False)
    response.raise_for_status()
    return response


def get_response(
    url: str,
) -> requests.models.Response:
    response = requests.post(
        url,
        verify=False,
        allow_redirects=False,
        timeout=current_app.config["REQUEST_TIMEOUT"],
    )
    response.raise_for_status()
    return response


def get_account_sites(
    response_data: requests.models.Response,
) -> t.List[t.Dict[str, str]]:
    data_content = json.loads(response_data.text)
    account_sites = [
        {"domain_name": f"https://{data['domain_name']}", "site_key": data["site_key"]}
        for data in data_content["result"]["data"]
    ]
    return account_sites


def check_script(response_data: requests.models.Response) -> bool:
    soup = BeautifulSoup(response_data.content, "html.parser")
    script = soup.find("script", attrs={"src": current_app.config["SCRIPT_STRING"]})
    return True if script else False


def check_site_key(response_data: requests.models.Response, site_key: str) -> bool:
    soup = BeautifulSoup(response_data.content, "html.parser")
    is_site_key = soup.find("script", text=re.compile(f".*{site_key}.*"))
    return True if is_site_key else False
