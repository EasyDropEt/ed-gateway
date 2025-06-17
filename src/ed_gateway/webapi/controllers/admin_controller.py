import asyncio
from typing import Annotated
from uuid import UUID

from ed_auth.application.features.auth.dtos import (LoginUserVerifyDto,
                                                    UnverifiedUserDto)
from ed_core.application.features.common.dtos import (BusinessDto, ConsumerDto,
                                                      DeliveryJobDto,
                                                      DriverDto, OrderDto)
from ed_core.documentation.api.abc_core_api_client import \
    AdminDto as CoreAdminDto
from ed_core.documentation.api.abc_core_api_client import (
    DriverPaymentSummaryDto, SettleDriverPaymentRequestDto, UpdateAdminDto)
from ed_domain.common.exceptions import ApplicationException, Exceptions
from ed_notification.documentation.api.abc_notification_api_client import \
    NotificationDto
from fastapi import APIRouter, Depends, WebSocket
from fastapi.security import HTTPAuthorizationCredentials
from rmediator import Mediator

from ed_gateway.application.features.admin.dtos import (AdminDto,
                                                        CreateAdminDto,
                                                        LoginAdminDto)
from ed_gateway.application.features.admin.requests.commands import (
    CreateAdminCommand, LoginAdminCommand, LoginAdminVerifyCommand,
    SettleDriverPaymentCommand, UpdateAdminCommand)
from ed_gateway.application.features.admin.requests.queries import (
    GetAdminByUserIdQuery, GetAdminsQuery, GetBusinessesQuery,
    GetConsumersQuery, GetDeliveryJobsQuery, GetDriversQuery, GetOrdersQuery)
from ed_gateway.application.features.drivers.dtos import CreateDriverAccountDto
from ed_gateway.application.features.drivers.requests.commands import \
    CreateDriverAccountCommand
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
router = APIRouter(prefix="")
config = get_config()
api_dep = get_api(config)
oauth2_scheme = JWTBearer(api_dep.auth_api)


@router.post(
    "/admin/register",
    response_model=GenericResponse[CoreAdminDto],
    tags=["Admin Auth"],
)
@rest_endpoint
async def create_account(
    mediator: Annotated[Mediator, Depends(mediator)],
    request: CreateAdminDto,
):
    LOG.info("Sending CreateAdminCommand to mediator with request: %s", request)
    return await mediator.send(CreateAdminCommand(request))


@router.post(
    "/admin/login/get-otp",
    response_model=GenericResponse[UnverifiedUserDto],
    tags=["Admin Auth"],
)
@rest_endpoint
async def login_admin(
    request: LoginAdminDto, mediator: Annotated[Mediator, Depends(mediator)]
):
    LOG.info("Sending LoginAdminCommand to mediator with request: %s", request)
    return await mediator.send(LoginAdminCommand(request))


@router.post(
    "/admin/login/verify",
    response_model=GenericResponse[AdminDto],
    tags=["Admin Auth"],
)
@rest_endpoint
async def login_admin_verify(
    request: LoginUserVerifyDto, mediator: Annotated[Mediator, Depends(mediator)]
):
    LOG.info("Sending LoginAdminVerifyCommand to mediator with request: %s", request)
    return await mediator.send(LoginAdminVerifyCommand(request))


@router.get(
    "/admin/me", response_model=GenericResponse[CoreAdminDto], tags=["Admin Features"]
)
@rest_endpoint
async def get_admin(
    mediator: Annotated[Mediator, Depends(mediator)],
    auth: Annotated[HTTPAuthorizationCredentials, Depends(oauth2_scheme)],
):
    LOG.info(
        "Sending GetAdminByUserIdQuery to mediator with user_id: %s",
        auth.credentials,
    )
    return await mediator.send(GetAdminByUserIdQuery(user_id=auth.credentials))


@router.get(
    "/admin/me", response_model=GenericResponse[CoreAdminDto], tags=["Admin Features"]
)
@rest_endpoint
async def update_admin(
    dto: UpdateAdminDto,
    mediator: Annotated[Mediator, Depends(mediator)],
    auth: Annotated[HTTPAuthorizationCredentials, Depends(oauth2_scheme)],
):
    admin_id = await _get_admin_id(auth.credentials, mediator)
    return await mediator.send(UpdateAdminCommand(admin_id, dto))


@router.post(
    "/admin/me/settle-driver-payment/{driver_id}",
    response_model=GenericResponse[DriverPaymentSummaryDto],
    tags=["Admin Features"],
)
@rest_endpoint
async def settle_driver_payment(
    driver_id: UUID,
    dto: SettleDriverPaymentRequestDto,
    mediator: Annotated[Mediator, Depends(mediator)],
    auth: Annotated[HTTPAuthorizationCredentials, Depends(oauth2_scheme)],
):
    admin_id = await _get_admin_id(auth.credentials, mediator)
    return await mediator.send(SettleDriverPaymentCommand(admin_id, driver_id, dto))


@router.get(
    "/admin/me/notifications",
    response_model=GenericResponse[list[NotificationDto]],
    tags=["Admin Features"],
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
    "/admin/me/notifications/{notification_id}/read",
    response_model=GenericResponse[NotificationDto],
    tags=["Admin Features"],
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


async def _get_admin_id(user_id: str, mediator: Mediator) -> UUID:
    response = (await mediator.send(GetAdminByUserIdQuery(user_id=user_id))).to_dict()

    if (
        not response["is_success"]
        or "data" not in response
        or "id" not in response["data"]
    ):
        raise ApplicationException(
            Exceptions.NotFoundException,
            "Admin not found.",
            response.get("errors", ["Failed to retrieve admin."]),
        )

    return response["data"]["id"]


@router.get(
    "/admins",
    response_model=GenericResponse[list[CoreAdminDto]],
    tags=["Admin Features"],
)
@rest_endpoint
async def get_admins(
    mediator: Annotated[Mediator, Depends(mediator)],
    auth: Annotated[HTTPAuthorizationCredentials, Depends(oauth2_scheme)],
):
    return await mediator.send(GetAdminsQuery())


@router.get(
    "/businesses",
    response_model=GenericResponse[list[BusinessDto]],
    tags=["Admin Features"],
)
@rest_endpoint
async def get_businesses(
    mediator: Annotated[Mediator, Depends(mediator)],
    auth: Annotated[HTTPAuthorizationCredentials, Depends(oauth2_scheme)],
):
    return await mediator.send(GetBusinessesQuery())


@router.get(
    "/consumers",
    response_model=GenericResponse[list[ConsumerDto]],
    tags=["Admin Features"],
)
@rest_endpoint
async def get_consumers(
    mediator: Annotated[Mediator, Depends(mediator)],
    auth: Annotated[HTTPAuthorizationCredentials, Depends(oauth2_scheme)],
):
    return await mediator.send(GetConsumersQuery())


@router.get(
    "/delivery-jobs",
    response_model=GenericResponse[list[DeliveryJobDto]],
    tags=["Admin Features"],
)
@rest_endpoint
async def get_delivery_jobs(
    mediator: Annotated[Mediator, Depends(mediator)],
    auth: Annotated[HTTPAuthorizationCredentials, Depends(oauth2_scheme)],
):
    return await mediator.send(GetDeliveryJobsQuery())


@router.get(
    "/drivers", response_model=GenericResponse[list[DriverDto]], tags=["Admin Features"]
)
@rest_endpoint
async def get_drivers(
    mediator: Annotated[Mediator, Depends(mediator)],
    auth: Annotated[HTTPAuthorizationCredentials, Depends(oauth2_scheme)],
):
    return await mediator.send(GetDriversQuery())


@router.get(
    "/orders", response_model=GenericResponse[list[OrderDto]], tags=["Admin Features"]
)
@rest_endpoint
async def get_orders(
    mediator: Annotated[Mediator, Depends(mediator)],
    auth: Annotated[HTTPAuthorizationCredentials, Depends(oauth2_scheme)],
):
    return await mediator.send(GetOrdersQuery())


@router.post(
    "/drivers",
    response_model=GenericResponse[DriverDto],
    tags=["Admin Features Auth"],
)
@rest_endpoint
async def create_driver_account(
    mediator: Annotated[Mediator, Depends(mediator)],
    request: CreateDriverAccountDto,
):
    LOG.info(
        "Sending CreateDriverAccountCommand to mediator with request: %s", request)
    return await mediator.send(
        CreateDriverAccountCommand(
            dto=request,
        )
    )
