import json
import pytest
from app import create_app

from app.api_app.handler import get_account_sites, check_script, check_site_key

app = create_app()


class TestResponse(object):
    pass


@pytest.fixture(scope="class")
def configure_app():
    app.config["API_URL"] = "https://dataapi.comagic.ru/v2.0"
    app.config["SITES_AMMOUNT"] = 40
    app.config["SERVER_NAME"] = "localhost"
    app.config["SCRIPT_STRING"] = "cs.min.js"


@pytest.mark.usefixtures("configure_app")
class TestHandler:
    @pytest.mark.parametrize(
        "test_response, expected_data",
        [
            (
                json.dumps(
                    {
                        "result": {
                            "data": [
                                {
                                    "site_key": "1actoZ_3xwRxvSlXn1OtVsDVEmikUtcV",
                                    "domain_name": "sitecmy.dev.uis.st",
                                },
                            ]
                        }
                    }
                ),
                [
                    {
                        "domain_name": "https://sitecmy.dev.uis.st",
                        "site_key": "1actoZ_3xwRxvSlXn1OtVsDVEmikUtcV",
                    },
                ],
            ),
        ],
    )
    def test_get_account_sites(self, test_response, expected_data):
        response = TestResponse()
        response.text = test_response
        account_sites = get_account_sites(response)
        assert expected_data == account_sites

    @pytest.mark.parametrize(
        "test_response, expected_data",
        [
            (
                """          
                    <html>
                    <head>
                    <script type="text/javascript" async src="https://app.comagic.ru/static/cs.min.js"></script>
                    <title>Comagic</title>
                    <meta charset=utf-8>
                    </head>
                    <body>
                    </body>
                    </html>
            """,
                True,
            ),
            (
                """          
                    <html>
                    <head>
                    <title>Comagic</title>
                    <meta charset=utf-8>
                    </head>
                    <body>
                    </body>
                    </html>
            """,
                False,
            ),
            (
                """          
                    <html>
                    <head>
                    <title>Comagic</title>
                    <script type="text/javascript" async src="https://app.comagic.ru/static/cs.min1.js"></script>
                    <meta charset=utf-8>
                    </head>
                    <body>
                    </body>
                    </html>
            """,
                False,
            ),
        ],
    )
    def test_check_script(self, test_response, expected_data):
        response = TestResponse()
        response.content = test_response
        with app.app_context():
            is_script = check_script(response)
        assert expected_data == is_script

    @pytest.mark.parametrize(
        "test_response, expected_data, site_key",
        [
            (
                """          
                    <html>
                    <head>
                    <title>Comagic</title>
                    <script type="text/javascript">
                        var __cs = __cs || [];
                        __cs.push(["setCsAccount", "Pxh6gEli88rX2iVg3NxP5ah7FdMfNTlC"]);
                        </script>
                    <meta charset=utf-8>
                    </head>
                    <body>
                    </body>
                    </html>
            """,
                True,
                "Pxh6gEli88rX2iVg3NxP5ah7FdMfNTlC",
            ),
            (
                """          
                    <html>
                    <head>
                    <title>Comagic</title>
                    <script type="text/javascript">
                        var __cs = __cs || [];
                        __cs.push(["setCsAccount", "Pxh6gEli88rX2idfdfvVg3NxP5ah7FdMfNTlC"]);
                        </script>
                    <meta charset=utf-8>
                    </head>
                    <body>
                    </body>
                    </html>
            """,
                False,
                "Pxh6gEli88rX2iVg3NxP5ah7FdMfNTlC",
            ),
            (
                """          
                    <html>
                    <head>
                    <title>Comagic</title>
                    <script type="text/javascript">
                        var __cs = __cs || [];
                        __cs.push(["setCsAccount", ]);
                        </script>
                    <meta charset=utf-8>
                    </head>
                    <body>
                    </body>
                    </html>
            """,
                False,
                "Pxh6gEli88rX2iVg3NxP5ah7FdMfNTlC",
            ),
        ],
    )
    def test_check_site_key(self, test_response, expected_data, site_key):
        response = TestResponse()
        response.content = test_response
        with app.app_context():
            is_site_key = check_site_key(response, site_key)
        assert expected_data == is_site_key
