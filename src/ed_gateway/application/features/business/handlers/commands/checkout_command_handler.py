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

LOG = get_logger()


@request_handler(CheckoutCommand, BaseResponse[OrderDto])
class CheckoutCommandHandler(RequestHandler):
    def __init__(self, api: ABCApi):
        self._api = api

        self._auth_service = AuthApiService(api.auth_api)

        self._error_message = "Order checkout cannot be initialized."
        self._success_message = "Order checkout initialized succesfully."

    async def handle(self, request: CheckoutCommand) -> BaseResponse[OrderDto]:
        dto = request.dto
        LOG.info(
            f"Calling core get_business_api_keys API with business_id: {request.api_key}"
        )
        response = await self._api.core_api.verify_api_key(request.api_key)

        LOG.info(f"Received response from get_business_api_keys: {response}")
        if response["is_success"] is False:
            raise ApplicationException(
                EXCEPTION_NAMES[response["http_status_code"]],
                self._error_message,
                response["errors"],
            )

        business = response["data"]

        user = await self._auth_service.create_or_get(
            {
                "first_name": dto["first_name"],
                "last_name": dto["last_name"],
                "email": dto["email"],
                "phone_number": dto["phone_number"],
            }
        )

        if user["new"]:
            consumer_response = await self._api.core_api.create_consumer(
                CreateConsumerDto(
                    user_id=user["id"],
                    first_name=dto["first_name"],
                    last_name=dto["last_name"],
                    email=dto["email"],
                    phone_number=dto["phone_number"],
                    location=dto["location"],
                )
            )
        else:
            consumer_response = await self._api.core_api.get_consumer_by_user_id(
                str(user["id"])
            )

        consumer = consumer_response["data"]
        LOG.info(
            f"Calling core create_business_orders API for business id: {business['id']} with order: {request.dto}"
        )
        create_order_dto = CreateOrderDto(
            consumer_id=consumer["id"],
            parcel=dto["parcel"],
            latest_time_of_delivery=dto["latest_time_of_delivery"],
        )
        response = await self._api.core_api.create_business_order(
            str(business["id"]), create_order_dto
        )

        LOG.info(f"Received response from create_business_orders: {response}")
        if not response["is_success"]:
            raise ApplicationException(
                EXCEPTION_NAMES[response["http_status_code"]],
                "Failed to create an order.",
                response["errors"],
            )

        prefix = request.api_key.split("_")[0]
        await self._api.core_api.delete_business_api_key(str(business["id"]), prefix)

        return BaseResponse[OrderDto].success(
            "Order created successfully.", response["data"]
        )
