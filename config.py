import os
from environs import Env


basedir = os.path.abspath(os.path.dirname(__file__))
env = Env()
env.read_env()

DEBUG = env.bool("DEBUG", True)

API_URL = "https://dataapi.comagic.ru/v2.0"
SITES_AMMOUNT = 40
ACCOUNT_ID = 1
REQUEST_TIMEOUT = 2
SCRIPT_STRING = "cs.min.js"
