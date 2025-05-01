from ed_core.documentation.abc_core_api_client import BusinessDto
from ed_domain.common.exceptions import ApplicationException, Exceptions
from rmediator.decorators import request_handler
from rmediator.types import RequestHandler

from ed_gateway.application.common.responses.base_response import BaseResponse
from ed_gateway.application.contracts.infrastructure.api.abc_api import ABCApi
from ed_gateway.application.features.business.requests.queries import \
    GetBusinessQuery
from ed_gateway.common.logging_helpers import get_logger

LOG = get_logger()


@request_handler(GetBusinessQuery, BaseResponse[BusinessDto])
class GetBusinessQueryHandler(RequestHandler):
    def __init__(self, api: ABCApi):
        self._api = api

    async def handle(self, request: GetBusinessQuery) -> BaseResponse[BusinessDto]:
        response = self._api.core_api.get_business(str(request.business_id))

        if not response["is_success"]:
            LOG.error(
                "Failed to fetch business.",
                request.business_id,
                response["errors"],
            )
            raise ApplicationException(
                Exceptions.InternalServerException,
                "Driver not found.",
                response["errors"],
            )

        return BaseResponse[BusinessDto].success(
            "Business fetched successfully.", response["data"]
        )
