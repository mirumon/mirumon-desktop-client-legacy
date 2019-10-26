import logging
from os.path import dirname, join

from dotenv import load_dotenv
from pydantic import BaseSettings
from pydantic.fields import Field

env_path = join(dirname(__file__), "..", ".env")
load_dotenv(env_path)


class Settings(BaseSettings):
    server_websocket_url: str = Field(..., env="SERVER_WEBSOCKET_URL")
    debug: bool = Field(False, env="DEBUG")


settings = Settings()
logging.basicConfig(level=logging.DEBUG if settings.debug else logging.INFO)
