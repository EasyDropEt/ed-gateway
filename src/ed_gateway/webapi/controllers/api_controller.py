from typing import Annotated

from ed_domain.common.exceptions import ApplicationException, Exceptions
from fastapi import APIRouter, Depends, Header, HTTPException
from rmediator import Mediator

from ed_gateway.application.features.business.dtos import CreateOrderDto
from ed_gateway.application.features.business.dtos.checkout_dto import \
    CheckoutDto
from ed_gateway.application.features.business.dtos.create_order_dto import \
    CreateParcelDto
from ed_gateway.application.features.business.requests.commands import (
    CheckoutCommand, InitializeCheckoutCommand)
from ed_gateway.common.logging_helpers import get_logger
from ed_gateway.webapi.common.helpers import GenericResponse, rest_endpoint
from ed_gateway.webapi.dependency_setup import mediator

LOG = get_logger()
router = APIRouter(prefix="/api", tags=["API Key Features"])


@router.post("/checkout/initialize", response_model=GenericResponse[CheckoutDto])
@rest_endpoint
async def initialize_checkout(
    dto: CreateParcelDto,
    mediator: Annotated[Mediator, Depends(mediator)],
    x_api_key: Annotated[str, Header(include_in_schema=True)],
    x_callback_url: Annotated[str, Header(include_in_schema=True)],
):
    LOG.info("Sending GetDeliveryJobsQuery to mediator")
    return await mediator.send(
        InitializeCheckoutCommand(x_api_key, x_callback_url, dto)
    )


@router.post("/checkout", response_model=GenericResponse[CheckoutDto])
@rest_endpoint
async def checkout(
    dto: CreateOrderDto,
    mediator: Annotated[Mediator, Depends(mediator)],
    x_api_key: Annotated[str, Header(include_in_schema=True)],
):

    LOG.info("Sending CheckoutCommand to mediator")
    return await mediator.send(CheckoutCommand(x_api_key, dto))
