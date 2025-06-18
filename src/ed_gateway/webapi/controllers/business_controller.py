import asyncio
from datetime import datetime
from typing import Annotated, Optional
from uuid import UUID

from ed_auth.documentation.api.abc_auth_api_client import (LoginUserVerifyDto,
                                                           UnverifiedUserDto)
from ed_core.application.features.common.dtos import WebhookDto
from ed_core.documentation.api.abc_core_api_client import (ApiKeyDto,
                                                           BusinessDto,
                                                           BusinessReportDto,
                                                           CreateApiKeyDto,
                                                           CreateWebhookDto,
                                                           OrderDto,
                                                           UpdateBusinessDto)
from ed_domain.common.exceptions import ApplicationException, Exceptions
from ed_notification.documentation.api.abc_notification_api_client import \
    NotificationDto
from fastapi import APIRouter, Depends, WebSocket
from fastapi.security import HTTPAuthorizationCredentials
from rmediator import Mediator

from ed_gateway.application.features.business.dtos import (
    BusinessAccountDto, CreateBusinessAccountDto, CreateOrderDto,
    LoginBusinessDto)
from ed_gateway.application.features.business.requests.commands import (
    CancelBusinessOrderCommand, CreateApiKeyCommand,
    CreateBusinessAccountCommand, CreateOrderCommand, CreateWebhookCommand,
    DeleteApiKeyCommand, LoginBusinessCommand, LoginBusinessVerifyCommand,
    UpdateBusinessCommand)
from ed_gateway.application.features.business.requests.queries import (
    GetBusinessApiKeysQuery, GetBusinessByUserIdQuery, GetBusinessOrdersQuery,
    GetBusinessReportQuery, GetBusinessWebhookQuery)
from ed_gateway.application.features.notifications.requests.commands import \
    ReadNotificationCommand
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
    "/me/profile",
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


@router.put(
    "/me/profile",
    response_model=GenericResponse[BusinessDto],
    tags=["Business Features"],
)
@rest_endpoint
async def update_business(
    dto: UpdateBusinessDto,
    mediator: Annotated[Mediator, Depends(mediator)],
    auth: Annotated[HTTPAuthorizationCredentials, Depends(oauth2_scheme)],
):
    business_id = await _get_business_id(auth.credentials, mediator)
    return await mediator.send(UpdateBusinessCommand(business_id, dto))


@router.get(
    "/me/notifications",
    response_model=GenericResponse[list[NotificationDto]],
    tags=["Business Features"],
)
@rest_endpoint
async def get_business_notifications(
    mediator: Annotated[Mediator, Depends(mediator)],
    auth: Annotated[HTTPAuthorizationCredentials, Depends(oauth2_scheme)],
):
    return await mediator.send(GetNotificationsQuery(UUID(auth.credentials)))


@router.post(
    "/me/webhook",
    response_model=GenericResponse[WebhookDto],
    tags=["Business Features"],
)
@rest_endpoint
async def create_webhook(
    dto: CreateWebhookDto,
    mediator: Annotated[Mediator, Depends(mediator)],
    auth: Annotated[HTTPAuthorizationCredentials, Depends(oauth2_scheme)],
):
    business_id = await _get_business_id(auth.credentials, mediator)
    return await mediator.send(CreateWebhookCommand(business_id, dto))


@router.get(
    "/me/webhook",
    response_model=GenericResponse[WebhookDto],
    tags=["Business Features"],
)
@rest_endpoint
async def get_webhook(
    mediator: Annotated[Mediator, Depends(mediator)],
    auth: Annotated[HTTPAuthorizationCredentials, Depends(oauth2_scheme)],
):
    business_id = await _get_business_id(auth.credentials, mediator)
    LOG.info(
        "Sending GetBusinessOrdersQuery to mediator with business_id: %s", business_id
    )
    return await mediator.send(GetBusinessWebhookQuery(business_id))


@router.post(
    "/me/api-keys",
    response_model=GenericResponse[ApiKeyDto],
    tags=["Business Features"],
)
@rest_endpoint
async def create_api_key(
    dto: CreateApiKeyDto,
    mediator: Annotated[Mediator, Depends(mediator)],
    auth: Annotated[HTTPAuthorizationCredentials, Depends(oauth2_scheme)],
):
    business_id = await _get_business_id(auth.credentials, mediator)
    return await mediator.send(CreateApiKeyCommand(business_id, dto))


@router.get(
    "/me/api-keys",
    response_model=GenericResponse[list[ApiKeyDto]],
    tags=["Business Features"],
)
@rest_endpoint
async def get_api_keys(
    mediator: Annotated[Mediator, Depends(mediator)],
    auth: Annotated[HTTPAuthorizationCredentials, Depends(oauth2_scheme)],
):
    business_id = await _get_business_id(auth.credentials, mediator)
    LOG.info(
        "Sending GetBusinessOrdersQuery to mediator with business_id: %s", business_id
    )
    return await mediator.send(GetBusinessApiKeysQuery(business_id))


@router.delete(
    "/me/api-keys/{api_key_prefix}",
    response_model=GenericResponse[None],
    tags=["Business Features"],
)
@rest_endpoint
async def delete_api_key(
    api_key_prefix: str,
    mediator: Annotated[Mediator, Depends(mediator)],
    auth: Annotated[HTTPAuthorizationCredentials, Depends(oauth2_scheme)],
):
    business_id = await _get_business_id(auth.credentials, mediator)
    LOG.info(
        "Sending DeleteApiKeyCommand to mediator with business_id: %s, api_key_prefix: %s",
        business_id,
        api_key_prefix,
    )
    return await mediator.send(DeleteApiKeyCommand(business_id, api_key_prefix))


@router.get(
    "/me/report",
    response_model=GenericResponse[BusinessReportDto],
    tags=["Business Features"],
)
@rest_endpoint
async def get_report(
    mediator: Annotated[Mediator, Depends(mediator)],
    auth: Annotated[HTTPAuthorizationCredentials, Depends(oauth2_scheme)],
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
):
    business_id = await _get_business_id(auth.credentials, mediator)
    LOG.info(
        "Sending GetBusinessOrdersQuery to mediator with business_id: %s", business_id
    )
    return await mediator.send(
        GetBusinessReportQuery(business_id, start_date, end_date)
    )


@router.post(
    "/me/orders",
    response_model=GenericResponse[OrderDto],
    tags=["Business Features"],
)
@rest_endpoint
async def create_order(
    request: CreateOrderDto,
    mediator: Annotated[Mediator, Depends(mediator)],
    auth: Annotated[HTTPAuthorizationCredentials, Depends(oauth2_scheme)],
):

    business_id = await _get_business_id(auth.credentials, mediator)
    LOG.info(
        "Sending CreateOrdersCommand to mediator with business_id: %s and request: %s",
        business_id,
        request,
    )
    return await mediator.send(CreateOrderCommand(business_id, dto=request))


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
    return await mediator.send(GetBusinessOrdersQuery(business_id))


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
    return await mediator.send(CancelBusinessOrderCommand(business_id, order_id))


@router.get(
    "/me/notifications",
    response_model=GenericResponse[list[NotificationDto]],
    tags=["Business Features"],
)
@rest_endpoint
async def get_notifications(
    mediator: Annotated[Mediator, Depends(mediator)],
    auth: Annotated[HTTPAuthorizationCredentials, Depends(oauth2_scheme)],
):
    LOG.info(
        "Sending GetNotificationsQuery to mediator with user_id: %s", auth.credentials
    )
    return await mediator.send(GetNotificationsQuery(UUID(auth.credentials)))


@router.put(
    "/me/notifications/{notification_id}/read",
    response_model=GenericResponse[NotificationDto],
    tags=["Business Features"],
)
@rest_endpoint
async def read_notification(
    notification_id: UUID,
    mediator: Annotated[Mediator, Depends(mediator)],
    auth: Annotated[HTTPAuthorizationCredentials, Depends(oauth2_scheme)],
):
    return await mediator.send(
        ReadNotificationCommand(UUID(auth.credentials), notification_id)
    )


@router.websocket("/{token}/notifications")
async def notfication_websocket(
    token: str,
    websocket: WebSocket,
    mediator: Annotated[Mediator, Depends(mediator)],
):
    auth = await oauth2_scheme.verify_token(token)
    await websocket.accept()

    while True:
        response = await mediator.send(GetNotificationsQuery(UUID(auth.credentials)))
        await websocket.send_json(response.to_dict())

        await asyncio.sleep(15)


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
