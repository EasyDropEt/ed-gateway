from ed_core.documentation.api.abc_core_api_client import (ABCCoreApiClient,
                                                           ConsumerDto,
                                                           CreateConsumerDto)
from ed_domain.common.exceptions import (EXCEPTION_NAMES, ApplicationException,
                                         Exceptions)
from ed_domain.common.logging import get_logger
from ed_domain.documentation.api.definitions import ApiResponse

LOG = get_logger()


class CoreApiService:
    def __init__(self, api: ABCCoreApiClient) -> None:
        self._api = api

    async def create_consumer(
        self, create_consumer_dto: CreateConsumerDto
    ) -> ConsumerDto:
        response = await self._api.create_consumer(create_consumer_dto)

    def _handle_response_errors(
        self, response: ApiResponse, error_message: str
    ) -> None:
        if "is_success" not in response:
            raise ApplicationException(
                Exceptions.InternalServerException,
                "Internal server exception.",
                [response["detail"]],
            )

        if not response["is_success"]:
            raise ApplicationException(
                EXCEPTION_NAMES[response["http_status_code"]],
                error_message,
                [response["errors"]],
            )
