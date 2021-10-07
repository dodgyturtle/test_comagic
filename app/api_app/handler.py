import typing as t
import json
import requests

JSONType = t.Union[str, int, float, bool, None, t.Dict[str, t.Any], t.List[t.Any]]

def post_response(url: str, data: JSONType = None) -> requests.models.Response:
    response = requests.post(url, data=data, verify=False, allow_redirects=False)
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
