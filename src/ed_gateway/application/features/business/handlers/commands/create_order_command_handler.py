from ed_core.documentation.api.abc_core_api_client import OrderDto
from rmediator.decorators import request_handler
from rmediator.types import RequestHandler

from ed_gateway.application.common.responses.base_response import BaseResponse
from ed_gateway.application.contracts.infrastructure.api.abc_api import ABCApi
from ed_gateway.application.features.business.requests.commands import \
    CreateOrderCommand
from ed_gateway.application.service.api_service import ApiService
from ed_gateway.application.service.auth_api_service import AuthApiService
from ed_gateway.common.logging_helpers import get_logger

LOG = get_logger()


@request_handler(CreateOrderCommand, BaseResponse[OrderDto])
class CreateOrderCommandHandler(RequestHandler):
    def __init__(self, api_handler: ABCApi):
        self._api_handler = api_handler
        self._auth_service = AuthApiService(api_handler.auth_api)

        self._error_message = "Failed to create order."
        self._success_message = "Order created successfully."

        self._api_service = ApiService(self._error_message)

    async def handle(self, request: CreateOrderCommand) -> BaseResponse[OrderDto]:
        dto = request.dto
        user = await self._auth_service.create_or_get(
            {
                "first_name": dto["first_name"],
                "last_name": dto["last_name"],
                "email": dto["email"],
                "phone_number": dto["phone_number"],
            }
        )

        consumer_response = await self._api_handler.core_api.get_consumer_by_user_id(
            str(user["id"])
        )
        self._api_service.basic_verify(consumer_response)

        if not consumer_response["is_success"]:
            consumer_response = await self._api_handler.core_api.create_consumer(
                {
                    "user_id": user["id"],
                    "first_name": dto["first_name"],
                    "last_name": dto["last_name"],
                    "email": dto["email"],
                    "phone_number": dto["phone_number"],
                    "location": dto["location"],
                }
            )
            self._api_service.verify(consumer_response)

        consumer = consumer_response["data"]
        LOG.info(
            f"Calling core create_business_orders API for business id: {request.business_id} with orders: {request.dto}"
        )
        response = await self._api_handler.core_api.create_business_order(
            str(request.business_id),
            {
                "consumer_id": consumer["id"],
                "parcel": dto["parcel"],
                "latest_time_of_delivery": dto["latest_time_of_delivery"],
            },
        )
        self._api_service.verify(response)

        return BaseResponse[OrderDto].success(self._success_message, response["data"])
