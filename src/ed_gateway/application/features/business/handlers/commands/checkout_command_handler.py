from ed_core.application.features.business.dtos import CreateOrderDto
from ed_core.application.features.common.dtos import (CreateConsumerDto,
                                                      OrderDto)
from ed_domain.common.exceptions import EXCEPTION_NAMES, ApplicationException
from rmediator.decorators import request_handler
from rmediator.types import RequestHandler

from ed_gateway.application.common.responses.base_response import BaseResponse
from ed_gateway.application.contracts.infrastructure.api.abc_api import ABCApi
from ed_gateway.application.features.business.requests.commands import \
    CheckoutCommand
from ed_gateway.application.service.auth_api_service import AuthApiService
from ed_gateway.common.logging_helpers import get_logger
from src.ed_gateway.application.service.api_service import ApiService

LOG = get_logger()


@request_handler(CheckoutCommand, BaseResponse[OrderDto])
class CheckoutCommandHandler(RequestHandler):
    def __init__(self, api: ABCApi):
        self._api = api

        self._auth_service = AuthApiService(api.auth_api)

        self._error_message = "Order checkout failed."
        self._success_message = "Order checkout completed succesfully."

        self._api_service = ApiService(self._error_message)

    async def handle(self, request: CheckoutCommand) -> BaseResponse[OrderDto]:
        dto = request.dto

        LOG.info(
            f"Calling core get_business_api_keys API with business_id: {request.api_key}"
        )
        response = await self._api.core_api.verify_api_key(request.api_key)
        LOG.info(f"Received response from get_business_api_keys: {response}")
        self._api_service.verify(response)
        business = response["data"]

        user = await self._auth_service.create_or_get(
            {
                "first_name": dto["first_name"],
                "last_name": dto["last_name"],
                "email": dto["email"],
                "phone_number": dto["phone_number"],
            }
        )

        consumer_response = await self._api.core_api.get_consumer_by_user_id(
            str(user["id"])
        )
        self._api_service.basic_verify(consumer_response)

        if not consumer_response["is_success"]:
            consumer_response = await self._api.core_api.create_consumer(
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
            f"Calling core create_business_orders API for business id: {business['id']} with orders: {request.dto}"
        )
        parcel_size = dto["parcel"]["size"].value
        response = await self._api.core_api.create_business_order(
            str(business["id"]),
            {
                "consumer_id": consumer["id"],
                "parcel": {
                    **dto["parcel"],
                    "size": parcel_size,  # type: ignore
                },
                "latest_time_of_delivery": dto["latest_time_of_delivery"],
            },
        )
        self._api_service.verify(response)

        return BaseResponse[OrderDto].success(self._success_message, response["data"])
