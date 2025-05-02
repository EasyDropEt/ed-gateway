from ed_gateway.common.logging_helpers import get_logger
from ed_gateway.webapi.api import API

LOG = get_logger()


class Package:
    def __init__(self) -> None:
        self._api = API(
            title="ED Gateway API",
            description="ED Gateway API Documentation",
            version="1.0.0",
        )

    def start(self) -> None:
        self._api.start()

    def stop(self) -> None:
        self._api.stop()


if __name__ == "__main__":
    main = Package()
    main.start()
