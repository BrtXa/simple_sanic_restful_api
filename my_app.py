import os

from sanic import *
from sanic.response import text
from sanic_openapi.openapi2 import doc, openapi2_blueprint

from api import api
from databases.db_config import DBConfig
from databases.pymongo import MongoDB


class Config:
    RUN_SETTING = {
        "host": os.environ.get("SERVER_HOST", "localhost"),
        "port": int(os.environ.get("SERVER_PORT", 8000)),
        "debug": False,
        "access_log": True,
        "auto_reload": True,
        "workers": 4,
    }
    # uWSGI를 통해 배포되어야 하므로, production level에선 run setting을 건드리지 않음
    SECRET_UUID = os.environ.get("SECRET_UUID", "cross-chain-identification")
    SECRET_KEY = os.environ.get("SECRET_KEY", "cross-chain-identification")
    EXPIRATION_JWT = 2592000  # seconds
    RESPONSE_TIMEOUT = 900  # seconds

    API_HOST = os.getenv("API_HOST", "0.0.0.0:8000")
    API_SCHEMES = os.getenv("API_SCHEMES", "http")
    API_VERSION = os.getenv("API_VERSION", "0.1.0")
    API_TITLE = os.getenv("API_TITLE", "CROSS CHAIN IDENTIFICATION API")
    API_DESCRIPTION = os.getenv(
        "API_DESCRIPTION", "An example Swagger for cross chain identification"
    )
    API_CONTACT_EMAIL = os.getenv("API_CONTACT_EMAIL", "example@gmail.com")


# App instance.
my_app = Sanic(__name__)
# my_app.blueprint(api)

my_app.blueprint(openapi2_blueprint)
my_app.config["API_HOST"] = Config.API_HOST
my_app.config["API_SCHEMES"] = Config.API_SCHEMES
my_app.config["API_TITLE"] = Config.API_TITLE
my_app.config["API_VERSION"] = Config.API_VERSION
my_app.config["API_DESCRIPTION"] = Config.API_DESCRIPTION
my_app.config["API_CONTACT_EMAIL"] = Config.API_CONTACT_EMAIL

my_app.config["RESPONSE_TIMEOUT"] = Config.RESPONSE_TIMEOUT

# Database.
db = MongoDB(DBConfig.MongoDB_URI, DBConfig.MongoDB_DB_NAME)

my_app.blueprint(api)


@my_app.get("/")
@doc.tag("Test")
async def hello_world(request):
    return text("Hello, World!")


def main():
    my_app.run(debug=True)


if __name__ == "__main__":
    main()
