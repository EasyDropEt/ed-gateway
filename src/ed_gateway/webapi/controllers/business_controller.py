from typing import Annotated
from uuid import UUID

from ed_auth.application.features.auth.dtos import (LoginUserVerifyDto,
                                                    UnverifiedUserDto)
from ed_core.documentation.abc_core_api_client import (BusinessDto,
                                                       CreateOrdersDto,
                                                       NotificationDto,
                                                       OrderDto)
from ed_domain.common.exceptions import ApplicationException, Exceptions
from fastapi import APIRouter, Depends
from fastapi.security import HTTPAuthorizationCredentials
from rmediator import Mediator

from ed_gateway.application.features.business.dtos import (
    BusinessAccountDto, CreateBusinessAccountDto, LoginBusinessDto)
from ed_gateway.application.features.business.requests.commands import (
    CancelBusinessOrderCommand, CreateBusinessAccountCommand,
    CreateOrdersCommand, LoginBusinessCommand, LoginBusinessVerifyCommand)
from ed_gateway.application.features.business.requests.queries import (
    GetBusinessByUserIdQuery, GetBusinessOrdersQuery)
from ed_gateway.application.features.notifications.requests.queries import \
    GetNotificationsQuery
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
    LOG.info(
        "Sending CreateBusinessAccountCommand to mediator with request: %s", request
    )
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
    LOG.info("Sending LoginBusinessCommand to mediator with request: %s", request)
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
    LOG.info(
        "Sending LoginBusinessVerifyCommand to mediator with request: %s", request)
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
    LOG.info(
        "Sending GetBusinessByUserIdQuery to mediator with user_id: %s",
        auth.credentials,
    )
    return await mediator.send(GetBusinessByUserIdQuery(user_id=auth.credentials))


@router.get(
    "/me/notifications",
    response_model=GenericResponse[list[NotificationDto]],
    tags=["Business Features"],
)
@rest_endpoint
# Notifications are scoped to the user account (user_id), not to a business.
async def get_business_notifications(
    mediator: Annotated[Mediator, Depends(mediator)],
    auth: Annotated[HTTPAuthorizationCredentials, Depends(oauth2_scheme)],
):

    LOG.info(
        "Sending GetNotificationsQuery to mediator with user_id: %s", auth.credentials
    )
    return await mediator.send(GetNotificationsQuery(UUID(auth.credentials)))


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

    business_id = await _get_business_id(auth.credentials, mediator)
    LOG.info(
        "Sending CreateOrdersCommand to mediator with business_id: %s and request: %s",
        business_id,
        request,
    )
    return await mediator.send(
        CreateOrdersCommand(business_id=business_id, dto=request)
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
    business_id = await _get_business_id(auth.credentials, mediator)
    LOG.info(
        "Sending GetBusinessOrdersQuery to mediator with business_id: %s", business_id
    )
    return await mediator.send(GetBusinessOrdersQuery(business_id=business_id))


@router.post(
    "/me/orders/{order_id}/cancel",
    response_model=GenericResponse[OrderDto],
    tags=["Business Features"],
)
@rest_endpoint
async def cancel_order(
    order_id: UUID,
    mediator: Annotated[Mediator, Depends(mediator)],
    auth: Annotated[HTTPAuthorizationCredentials, Depends(oauth2_scheme)],
):
    business_id = await _get_business_id(auth.credentials, mediator)
    return await mediator.send(
        CancelBusinessOrderCommand(business_id=business_id, order_id=order_id)
    )


async def _get_business_id(user_id: str, mediator: Mediator) -> UUID:
    response = (
        await mediator.send(GetBusinessByUserIdQuery(user_id=user_id))
    ).to_dict()

    if (
        not response["is_success"]
        or "data" not in response
        or "id" not in response["data"]
    ):
        raise ApplicationException(
            Exceptions.NotFoundException,
            "Business not found.",
            response.get("errors", ["Failed to retrieve driver."]),
        )

    return response["data"]["id"]
