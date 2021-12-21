import os
from os.path import dirname, isfile, join

from dotenv import load_dotenv

class Config(object):
    DEBUG=True
    RESTFUL_JSON = {
    'ensure_ascii': False
    }
    SQLALCHEMY_DATABASE_URI= os.getenv('DATABASE_URL')
    # trocar postgres por postgresql
    indexPostgres = SQLALCHEMY_DATABASE_URI.index("postgres")
    lenPostgres = 8
    SQLALCHEMY_DATABASE_URI= "".join(["postgresql", SQLALCHEMY_DATABASE_URI[indexPostgres+lenPostgres:]])
    SQLALCHEMY_TRACK_MODIFICATIONS=False
    TASK_PAGE_SIZE = 6

class Production(Config):
    DEBUG=False
    TASK_PAGE_SIZE = 10
    PROPAGATE_EXCEPTIONS = True

class Development(Config):
    DEBUG=True
    TASK_PAGE_SIZE = 5

config = {"development": Development, \
        "production": Production}
