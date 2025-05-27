from ed_core.documentation.api.abc_core_api_client import BusinessDto
from ed_domain.common.exceptions import ApplicationException, EXCEPTION_NAMES
from rmediator.decorators import request_handler
from rmediator.types import RequestHandler

from ed_gateway.application.common.responses.base_response import BaseResponse
from ed_gateway.application.contracts.infrastructure.api.abc_api import ABCApi
from ed_gateway.application.features.business.requests.queries import \
    GetBusinessByUserIdQuery
from ed_gateway.common.logging_helpers import get_logger

LOG = get_logger()


@request_handler(GetBusinessByUserIdQuery, BaseResponse[BusinessDto])
class GetBusinessByUserIdQueryHandler(RequestHandler):
    def __init__(self, api: ABCApi):
        self._api = api

    async def handle(
        self, request: GetBusinessByUserIdQuery
    ) -> BaseResponse[BusinessDto]:
        LOG.info(
            f"Calling core get_business_by_user_id API with user_id: {request.user_id}"
        )
        response = self._api.core_api.get_business_by_user_id(request.user_id)

        LOG.info(f"Received response from get_business_by_user_id: {response}")
        if not response["is_success"]:

            raise ApplicationException(
                EXCEPTION_NAMES[response["http_status_code"]],
                "Business not found.",
                response["errors"],
            )

        return BaseResponse[BusinessDto].success(
            "Business fetched successfully.", response["data"]
        )
