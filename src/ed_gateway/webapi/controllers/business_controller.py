from typing import Annotated
from uuid import UUID

from ed_auth.application.features.auth.dtos import (LoginUserVerifyDto,
                                                    UnverifiedUserDto)
from ed_core.documentation.abc_core_api_client import (BusinessDto,
                                                       CreateOrdersDto)
from fastapi import APIRouter, Depends
from rmediator import Mediator

from ed_gateway.application.features.business.dtos import (
    BusinessAccountDto, CreateBusinessAccountDto, LoginBusinessDto)
from ed_gateway.application.features.business.requests.commands import (
    CreateBusinessAccountCommand, CreateOrdersCommand, LoginBusinessCommand,
    LoginBusinessVerifyCommand)
from ed_gateway.application.features.business.requests.queries import (
    GetBusinessOrdersQuery, GetBusinessQuery)
from ed_gateway.common.logging_helpers import get_logger
from ed_gateway.webapi.common.helpers import GenericResponse, rest_endpoint
from ed_gateway.webapi.dependency_setup import mediator

LOG = get_logger()
router = APIRouter(prefix="/business", tags=["Business Features"])


@router.post("", response_model=GenericResponse[BusinessAccountDto])
@rest_endpoint
async def create_account(
    request: CreateBusinessAccountDto, mediator: Annotated[Mediator, Depends(mediator)]
):
    return await mediator.send(CreateBusinessAccountCommand(dto=request))


@router.post("/login/get-otp", response_model=GenericResponse[UnverifiedUserDto])
@rest_endpoint
async def login_business(
    request: LoginBusinessDto, mediator: Annotated[Mediator, Depends(mediator)]
):
    return await mediator.send(LoginBusinessCommand(dto=request))


@router.post("/login/verify", response_model=GenericResponse[BusinessDto])
@rest_endpoint
async def login_business_verify(
    request: LoginUserVerifyDto, mediator: Annotated[Mediator, Depends(mediator)]
):
    return await mediator.send(LoginBusinessVerifyCommand(dto=request))


@router.get("/{business_id}", response_model=GenericResponse[BusinessAccountDto])
@rest_endpoint
async def get_business(
    business_id: UUID, mediator: Annotated[Mediator, Depends(mediator)]
):
    return await mediator.send(GetBusinessQuery(business_id=business_id))


@router.post(
    "/{business_id}/orders", response_model=GenericResponse[BusinessAccountDto]
)
@rest_endpoint
async def create_orders(
    business_id: UUID,
    request: CreateOrdersDto,
    mediator: Annotated[Mediator, Depends(mediator)],
):
    return await mediator.send(
        CreateOrdersCommand(business_id=business_id, dto=request)
    )


@router.get("/{business_id}/orders", response_model=GenericResponse[list[OrderDto]])
@rest_endpoint
async def get_orders(
    business_id: UUID, mediator: Annotated[Mediator, Depends(mediator)]
):
    return await mediator.send(GetBusinessOrdersQuery(business_id=business_id))
