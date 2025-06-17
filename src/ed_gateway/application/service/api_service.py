from ed_domain.common.exceptions import (EXCEPTION_NAMES, ApplicationException,
                                         Exceptions)
from ed_domain.common.logging import get_logger
from ed_domain.documentation.api.definitions import ApiResponse

LOG = get_logger()


class ApiService:
    def __init__(self, error_message: str) -> None:
        self._error_message = error_message

    def basic_verify(
        self, response: ApiResponse | dict, error_message: str = "Some error occured."
    ) -> None:
        LOG.info(f"Verifying response: {response}")

        if "is_success" not in response:
            raise ApplicationException(
                Exceptions.InternalServerException,
                self._error_message,
                [response["detail"]],
            )

    def verify(self, response: ApiResponse | dict) -> None:
        LOG.info(f"Verifying response: {response}")

        if "is_success" not in response:
            raise ApplicationException(
                Exceptions.InternalServerException,
                self._error_message,
                [response["detail"]],
            )

        if not response["is_success"]:
            raise ApplicationException(
                EXCEPTION_NAMES[response["http_status_code"]],
                self._error_message,
                response["errors"],
            )
