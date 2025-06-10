from typing import Annotated
from uuid import UUID

from ed_auth.application.features.auth.dtos import (LoginUserVerifyDto,
                                                    UnverifiedUserDto)
from ed_core.documentation.api.abc_core_api_client import \
    ConsumerDto as CoreConsumerDto
from ed_core.documentation.api.abc_core_api_client import OrderDto
from ed_domain.common.exceptions import ApplicationException, Exceptions
from fastapi import APIRouter, Depends
from fastapi.security import HTTPAuthorizationCredentials
from rmediator import Mediator

from ed_gateway.application.features.consumers.dtos import (ConsumerDto,
                                                            CreateConsumerDto,
                                                            LoginConsumerDto)
from ed_gateway.application.features.consumers.requests.commands import (
    CreateConsumerCommand, LoginConsumerCommand, LoginConsumerVerifyCommand)
from ed_gateway.application.features.consumers.requests.queries import (
    GetConsumerByUserIdQuery, GetConsumerOrdersQuery)
from ed_gateway.common.generic_helpers import get_config
from ed_gateway.common.logging_helpers import get_logger
from ed_gateway.webapi.common.helpers import GenericResponse, rest_endpoint
from ed_gateway.webapi.common.jwt_bearer import JWTBearer
from ed_gateway.webapi.dependency_setup import api as get_api
from ed_gateway.webapi.dependency_setup import mediator

LOG = get_logger()
router = APIRouter(prefix="/consumers")
config = get_config()
api_dep = get_api(config)
oauth2_scheme = JWTBearer(api_dep.auth_api)


@router.post(
    "/register",
    response_model=GenericResponse[CoreConsumerDto],
    tags=["Consumer Auth"],
)
@rest_endpoint
async def create_account(
    mediator: Annotated[Mediator, Depends(mediator)],
    request: CreateConsumerDto,
):
    LOG.info("Sending CreateConsumerCommand to mediator with request: %s", request)
    return await mediator.send(
        CreateConsumerCommand(
            dto=request,
        )
    )


@router.post(
    "/login/get-otp",
    response_model=GenericResponse[UnverifiedUserDto],
    tags=["Consumer Auth"],
)
@rest_endpoint
async def login_consumer(
    request: LoginConsumerDto, mediator: Annotated[Mediator, Depends(mediator)]
):
    LOG.info("Sending LoginConsumerCommand to mediator with request: %s", request)
    return await mediator.send(LoginConsumerCommand(dto=request))


@router.post(
    "/login/verify",
    response_model=GenericResponse[ConsumerDto],
    tags=["Consumer Auth"],
)
@rest_endpoint
async def login_consumer_verify(
    request: LoginUserVerifyDto, mediator: Annotated[Mediator, Depends(mediator)]
):
    LOG.info(
        "Sending LoginConsumerVerifyCommand to mediator with request: %s", request)
    return await mediator.send(LoginConsumerVerifyCommand(dto=request))


@router.get(
    "/me", response_model=GenericResponse[CoreConsumerDto], tags=["Consumer Features"]
)
@rest_endpoint
async def get_consumer(
    mediator: Annotated[Mediator, Depends(mediator)],
    auth: Annotated[HTTPAuthorizationCredentials, Depends(oauth2_scheme)],
):
    LOG.info(
        "Sending GetConsumerByUserIdQuery to mediator with user_id: %s",
        auth.credentials,
    )
    return await mediator.send(GetConsumerByUserIdQuery(user_id=auth.credentials))


@router.get(
    "/me/orders",
    response_model=GenericResponse[list[OrderDto]],
    tags=["Consumer Features"],
)
@rest_endpoint
async def get_consumer_delivery_jobs(
    mediator: Annotated[Mediator, Depends(mediator)],
    auth: Annotated[HTTPAuthorizationCredentials, Depends(oauth2_scheme)],
):
    consumer_id = await _get_consumer_id(auth.credentials, mediator)
    return await mediator.send(GetConsumerOrdersQuery(consumer_id=consumer_id))


async def _get_consumer_id(user_id: str, mediator: Mediator) -> UUID:
    response = (
        await mediator.send(GetConsumerByUserIdQuery(user_id=user_id))
    ).to_dict()

    if (
        not response["is_success"]
        or "data" not in response
        or "id" not in response["data"]
    ):
        raise ApplicationException(
            Exceptions.NotFoundException,
            "Consumer not found.",
            response.get("errors", ["Failed to retrieve consumer."]),
        )

    return response["data"]["id"]
