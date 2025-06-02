from ed_core.documentation.api.abc_core_api_client import BusinessDto
from ed_domain.common.exceptions import ApplicationException, EXCEPTION_NAMES
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
        LOG.info(
            f"Calling core get_business API with business_id: {request.business_id}"
        )
        response = await self._api.core_api.get_business(str(request.business_id))

        LOG.info(f"Received response from get_business: {response}")
        if not response["is_success"]:
            raise ApplicationException(
                EXCEPTION_NAMES[response["http_status_code"]],
                "Driver not found.",
                response["errors"],
            )

        return BaseResponse[BusinessDto].success(
            "Business fetched successfully.", response["data"]
        )
