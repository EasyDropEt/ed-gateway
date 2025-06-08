from ed_core.documentation.api.abc_core_api_client import OrderDto
from ed_domain.common.exceptions import EXCEPTION_NAMES, ApplicationException
from rmediator.decorators import request_handler
from rmediator.types import RequestHandler

from ed_gateway.application.common.responses.base_response import BaseResponse
from ed_gateway.application.contracts.infrastructure.api.abc_api import ABCApi
from ed_gateway.application.features.business.requests.commands import \
    CreateOrderCommand
from ed_gateway.common.logging_helpers import get_logger

LOG = get_logger()


@request_handler(CreateOrderCommand, BaseResponse[OrderDto])
class CreateOrderCommandHandler(RequestHandler):
    def __init__(self, api_handler: ABCApi):
        self._api_handler = api_handler

    async def handle(self, request: CreateOrderCommand) -> BaseResponse[OrderDto]:
        create_consumer_dto = request.dto.consumer_id

        LOG.info(
            f"Callign auth create_or_get_user API for consumer {create_consumer_dto}"
        )
        auth_response = await self._api_handler.auth_api.create_or_get_user(
            {
                "first_name": create_consumer_dto.first_name,
                "last_name": create_consumer_dto.last_name,
                "email": create_consumer_dto.email,
                "phone_number": create_consumer_dto.phone_number,
            }
        )

        LOG.info(f"Received response from create_or_get_user: {auth_response}")
        if not auth_response["is_success"]:
            LOG.error(
                "Failed to create a user.",
                request.business_id,
                auth_response["errors"],
            )
            raise ApplicationException(
                EXCEPTION_NAMES[auth_response["http_status_code"]],
                "Failed to create an order.",
                auth_response["errors"],
            )

        request.dto.consumer_id.user_id = auth_response["data"]["id"]

        LOG.info(
            f"Calling core create_business_orders API for business id: {request.business_id} with orders: {request.dto}"
        )
        response = await self._api_handler.core_api.create_business_order(
            str(request.business_id), request.dto
        )

        LOG.info(f"Received response from create_business_orders: {response}")
        if not response["is_success"]:
            LOG.error(
                "Failed to create an order.",
                request.business_id,
                response["errors"],
            )
            raise ApplicationException(
                EXCEPTION_NAMES[response["http_status_code"]],
                "Failed to create an order.",
                response["errors"],
            )

        return BaseResponse[OrderDto].success(
            "Orders created successfully.", response["data"]
        )
