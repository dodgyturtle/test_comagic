import json
from typing import Any, Callable

from flask import Blueprint, current_app, request, url_for, wrappers
from marshmallow import ValidationError

from .handler import get_account_sites, post_response
from .schemes import AccountSchema, SiteSchema

api_blueprint = Blueprint("api", __name__)


@api_blueprint.app_errorhandler(500)
def internal_server_error(e):
    return {"message": "Internal Server Error"}, 500


@api_blueprint.app_errorhandler(404)
def send_url_not_found(e):
    return {"message": "URL not Found"}, 404


@api_blueprint.app_errorhandler(400)
def send_bad_request(e):
    return {
        "message": "400 Bad Request: The browser (or proxy) sent a request that this server could not understand"
    }, 400


@api_blueprint.route("/api/v1.0/account", methods=["POST"])
def get_sites() -> wrappers.Response:
    account_schema = AccountSchema()
    json_body = request.get_json()
    try:
        body = account_schema.load(json_body)
    except ValidationError as err:
        print(err.messages)
        return {"error": f"{ err.messages }"}, 400
    api_url = current_app.config["API_URL"]
    api_data = {
        "jsonrpc": "2.0",
        "id": current_app.config["ACCOUNT_ID"],
        "method": "get.sites",
        "params": {
            "access_token": body["access_token"],
            "offset": 0,
            "limit": current_app.config["SITES_AMMOUNT"],
        },
    }
    api_data_json = json.dumps(api_data)
    response = post_response(api_url, data=api_data_json)
    if "error" in response.text:
        error = json.loads(response.text)
        print(error["error"])
        return {"error": error["error"]["message"]}, 500
    account_sites = get_account_sites(response)
    return {"message": account_sites}, 200
