import os
from environs import Env


basedir = os.path.abspath(os.path.dirname(__file__))
env = Env()
env.read_env()

DEBUG = env.bool("DEBUG", True)
