import os
from os.path import dirname, isfile, join

from dotenv import load_dotenv

ENV_FILE = join(dirname(dirname(__file__)),'config.env')

if isfile(ENV_FILE):
    load_dotenv(dotenv_path=ENV_FILE)


class Config(object):
    DEBUG=True
    RESTFUL_JSON = {
    'ensure_ascii': False
    }
    SQLALCHEMY_DATABASE_URI= f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_DATABASE_NAME')}"
    SQLALCHEMY_TRACK_MODIFICATIONS=False
    TASK_PAGE_SIZE = 6

class Production(Config):
    DEBUG=False
    TASK_PAGE_SIZE = 10

class Development(Config):
    DEBUG=True
    TASK_PAGE_SIZE = 5

config = {"development": Development, \
        "production": Production}
