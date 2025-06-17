from ed_core.documentation.api.abc_core_api_client import BusinessDto
from ed_domain.common.exceptions import EXCEPTION_NAMES, ApplicationException
from rmediator.decorators import request_handler
from rmediator.types import RequestHandler

from ed_gateway.application.common.responses.base_response import BaseResponse
from ed_gateway.application.contracts.infrastructure.api.abc_api import ABCApi
from ed_gateway.application.features.admin.requests.queries import \
    GetBusinessesQuery
from ed_gateway.common.logging_helpers import get_logger

LOG = get_logger()


@request_handler(GetBusinessesQuery, BaseResponse[list[BusinessDto]])
class GetBusinessesQueryHandler(RequestHandler):
    def __init__(self, api: ABCApi):
        self._api = api

        self._success_message = "Businesses fetched successfully."
        self._error_message = "Failed to fetch businesses."

    async def handle(
        self, request: GetBusinessesQuery
    ) -> BaseResponse[list[BusinessDto]]:
        LOG.info("Calling core get_businesss API")
        response = await self._api.core_api.get_all_businesses()

        LOG.info(f"Received response from get_business: {response}")
        if not response["is_success"]:
            raise ApplicationException(
                EXCEPTION_NAMES[response["http_status_code"]],
                self._error_message,
                response["errors"],
            )

        return BaseResponse[list[BusinessDto]].success(
            self._success_message, response["data"]
        )
