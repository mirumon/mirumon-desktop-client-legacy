import logging

from pydantic import BaseSettings


class Settings(BaseSettings):
    server_websocket_url: str = "wss://api.mirumon.dev/clients/ws"  # ws://localhost:8000/clients/ws
    reconnect_delay: int = 10
    debug: bool = True

    class Config:  # noqa: WPS431
        case_sensitive = True


settings = Settings()

LOGGING_LEVEL = logging.DEBUG if settings.debug else logging.INFO
logging.basicConfig(level=LOGGING_LEVEL)
# logging.basicConfig(
#     handlers=[InterceptHandler(level=LOGGING_LEVEL)], level=LOGGING_LEVEL
# )
