from typing import Annotated

from ed_auth.application.features.auth.dtos import (LoginUserVerifyDto,
                                                    UnverifiedUserDto)
from ed_core.documentation.abc_core_api_client import (BusinessDto,
                                                       CreateOrdersDto,
                                                       OrderDto)
from fastapi import APIRouter, Depends
from fastapi.security import HTTPAuthorizationCredentials
from rmediator import Mediator

from ed_gateway.application.features.business.dtos import (
    BusinessAccountDto, CreateBusinessAccountDto, LoginBusinessDto)
from ed_gateway.application.features.business.requests.commands import (
    CreateBusinessAccountCommand, CreateOrdersCommand, LoginBusinessCommand,
    LoginBusinessVerifyCommand)
from ed_gateway.application.features.business.requests.queries import (
    GetBusinessByUserIdQuery, GetBusinessOrdersQuery)
from ed_gateway.common.generic_helpers import get_config
from ed_gateway.common.logging_helpers import get_logger
from ed_gateway.webapi.common.helpers import GenericResponse, rest_endpoint
from ed_gateway.webapi.common.jwt_bearer import JWTBearer
from ed_gateway.webapi.dependency_setup import api as get_api
from ed_gateway.webapi.dependency_setup import mediator

LOG = get_logger()
router = APIRouter(prefix="/business")
config = get_config()
api_dep = get_api(config)
oauth2_scheme = JWTBearer(api_dep.auth_api)


# Auth
@router.post(
    "/register",
    response_model=GenericResponse[BusinessDto],
    tags=["Business Auth"],
)
@rest_endpoint
async def create_account(
    request: CreateBusinessAccountDto, mediator: Annotated[Mediator, Depends(mediator)]
):
    return await mediator.send(CreateBusinessAccountCommand(dto=request))


@router.post(
    "/login/get-otp",
    response_model=GenericResponse[UnverifiedUserDto],
    tags=["Business Auth"],
)
@rest_endpoint
async def login_business(
    request: LoginBusinessDto, mediator: Annotated[Mediator, Depends(mediator)]
):
    return await mediator.send(LoginBusinessCommand(dto=request))


@router.post(
    "/login/verify",
    response_model=GenericResponse[BusinessAccountDto],
    tags=["Business Auth"],
)
@rest_endpoint
async def login_business_verify(
    request: LoginUserVerifyDto, mediator: Annotated[Mediator, Depends(mediator)]
):
    return await mediator.send(LoginBusinessVerifyCommand(dto=request))


@router.get(
    "/me",
    response_model=GenericResponse[BusinessDto],
    tags=["Business Features"],
)
@rest_endpoint
async def get_business(
    mediator: Annotated[Mediator, Depends(mediator)],
    auth: Annotated[HTTPAuthorizationCredentials, Depends(oauth2_scheme)],
):
    return await mediator.send(GetBusinessByUserIdQuery(user_id=auth.credentials))


@router.post(
    "/me/orders",
    response_model=GenericResponse[list[OrderDto]],
    tags=["Business Features"],
)
@rest_endpoint
async def create_orders(
    request: CreateOrdersDto,
    mediator: Annotated[Mediator, Depends(mediator)],
    auth: Annotated[HTTPAuthorizationCredentials, Depends(oauth2_scheme)],
):
    business = (
        await mediator.send(GetBusinessByUserIdQuery(user_id=auth.credentials))
    )["data"]
    return await mediator.send(
        CreateOrdersCommand(business_id=business["id"], dto=request)
    )


@router.get(
    "/me/orders",
    response_model=GenericResponse[list[OrderDto]],
    tags=["Business Features"],
)
@rest_endpoint
async def get_orders(
    mediator: Annotated[Mediator, Depends(mediator)],
    auth: Annotated[HTTPAuthorizationCredentials, Depends(oauth2_scheme)],
):
    business = (
        await mediator.send(GetBusinessByUserIdQuery(user_id=auth.credentials))
    )["data"]
    return await mediator.send(GetBusinessOrdersQuery(business_id=business["id"]))
