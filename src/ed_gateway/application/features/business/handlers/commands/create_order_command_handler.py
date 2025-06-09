from ed_core.application.features.common.dtos import CreateConsumerDto
from ed_core.documentation.api.abc_core_api_client import (CreateOrderDto,
                                                           OrderDto)
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
        dto = request.dto

        LOG.info(f"Calling auth create_or_get_user API for consumer {dto}")
        auth_response = await self._api_handler.auth_api.create_or_get_user(
            {
                "first_name": dto["first_name"],
                "last_name": dto["last_name"],
                "email": dto["email"],
                "phone_number": dto["phone_number"],
            }
        )

        LOG.info(f"Received response from create_or_get_user: {auth_response}")
        if not auth_response["is_success"]:
            raise ApplicationException(
                EXCEPTION_NAMES[auth_response["http_status_code"]],
                "Failed to create an order.",
                auth_response["errors"],
            )

        user = auth_response["data"]
        if user["new"]:
            consumer_response = await self._api_handler.core_api.create_consumer(
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
            consumer_response = (
                await self._api_handler.core_api.get_consumer_by_user_id(
                    str(user["id"])
                )
            )

        consumer = consumer_response["data"]
        LOG.info(
            f"Calling core create_business_orders API for business id: {request.business_id} with orders: {request.dto}"
        )
        dumped = CreateOrderDto(
            consumer_id=consumer["id"],  # type: ignore
            parcel=dto["parcel"],
            latest_time_of_delivery=dto["latest_time_of_delivery"],
        ).model_dump()

        print("DUMPED", dumped)
        response = await self._api_handler.core_api.create_business_order(
            str(request.business_id),
            dumped,  # type: ignore
        )

        LOG.info(f"Received response from create_business_orders: {response}")
        if not response["is_success"]:
            raise ApplicationException(
                EXCEPTION_NAMES[response["http_status_code"]],
                "Failed to create an order.",
                response["errors"],
            )

        return BaseResponse[OrderDto].success(
            "Orders created successfully.", response["data"]
        )
