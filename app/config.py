import logging
import sys
from os.path import dirname, join

from dotenv import load_dotenv
from loguru import logger
from pydantic import BaseSettings
from pydantic.fields import Field

from app.logging import InterceptHandler, format_record

env_path = join(dirname(__file__), "..", ".env")
load_dotenv(env_path)


class Settings(BaseSettings):
    server_websocket_url: str = Field(..., env="SERVER_WEBSOCKET_URL")
    debug: bool = Field(False, env="DEBUG")


settings = Settings()

LOGGING_LEVEL = logging.DEBUG if settings.debug else logging.INFO

logging.basicConfig(
    handlers=[InterceptHandler(level=LOGGING_LEVEL)], level=LOGGING_LEVEL
)
logger.configure(
    handlers=[{"sink": sys.stderr, "level": LOGGING_LEVEL, "format": format_record}]
)
