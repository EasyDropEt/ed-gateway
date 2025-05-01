from ed_core.documentation.abc_core_api_client import OrderDto
from rmediator.decorators import request_handler
from rmediator.types import RequestHandler

from ed_gateway.application.common.responses.base_response import BaseResponse
from ed_gateway.application.contracts.infrastructure.api.abc_api import ABCApi
from ed_gateway.application.features.business.requests.commands import \
    CreateOrdersCommand
from ed_gateway.common.exception_helpers import (ApplicationException,
                                                 Exceptions)
from ed_gateway.common.logging_helpers import get_logger

LOG = get_logger()


@request_handler(CreateOrdersCommand, BaseResponse[list[OrderDto]])
class CreateOrdersCommandHandler(RequestHandler):
    def __init__(self, api_handler: ABCApi):
        self._api_handler = api_handler

    async def handle(
        self, request: CreateOrdersCommand
    ) -> BaseResponse[list[OrderDto]]:
        LOG.info("Handling CreateOrdersCommand")
        response = self._api_handler.core_api.create_business_orders(
            str(request.business_id), request.dto
        )
        if not response["is_success"]:
            raise ApplicationException(
                Exceptions.InternalServerException,
                "Failed to create an order.",
                response["errors"],
            )

        return BaseResponse[list[OrderDto]].success(
            "Orders created successfully.", response["data"]
        )
