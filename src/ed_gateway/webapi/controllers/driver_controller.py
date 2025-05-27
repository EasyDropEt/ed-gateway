from typing import Annotated
from uuid import UUID

from ed_auth.application.features.auth.dtos import (LoginUserVerifyDto,
                                                    UnverifiedUserDto)
from ed_core.documentation.api.abc_core_api_client import (
    DeliveryJobDto, DriverDto, DriverHeldFundsDto, DriverPaymentSummaryDto,
    DropOffOrderDto, DropOffOrderVerifyDto, NotificationDto, OrderDto,
    PickUpOrderDto, PickUpOrderVerifyDto, UpdateLocationDto)
from ed_domain.common.exceptions import ApplicationException, Exceptions
from fastapi import APIRouter, Depends, WebSocket
from fastapi.security import HTTPAuthorizationCredentials
from rmediator import Mediator

from ed_gateway.application.features.drivers.dtos import (
    CreateDriverAccountDto, DriverAccountDto, LoginDriverDto)
from ed_gateway.application.features.drivers.requests.commands import (
    CancelDeliveryJobCommand, ClaimDeliveryJobCommand,
    CreateDriverAccountCommand, DropOffOrderCommand, DropOffOrderVerifyCommand,
    LoginDriverCommand, LoginDriverVerifyCommand, PickUpOrderCommand,
    PickUpOrderVerifyCommand, UpdateDriverCurrentLocationCommand)
from ed_gateway.application.features.drivers.requests.queries import (
    GetDriverByUserIdQuery, GetDriverDeliveryJobsQuery,
    GetDriverHeldFundsQuery, GetDriverOrdersQuery,
    GetDriverPaymentSummaryQuery)
from ed_gateway.application.features.notifications.requests.queries import \
    GetNotificationsQuery
from ed_gateway.common.generic_helpers import get_config
from ed_gateway.common.logging_helpers import get_logger
from ed_gateway.webapi.common.helpers import GenericResponse, rest_endpoint
from ed_gateway.webapi.common.jwt_bearer import JWTBearer
from ed_gateway.webapi.dependency_setup import api as get_api
from ed_gateway.webapi.dependency_setup import mediator

LOG = get_logger()
router = APIRouter(prefix="/drivers")
config = get_config()
api_dep = get_api(config)
oauth2_scheme = JWTBearer(api_dep.auth_api)


@router.post(
    "/register",
    response_model=GenericResponse[DriverAccountDto],
    tags=["Driver Auth"],
)
@rest_endpoint
async def create_account(
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


@router.post(
    "/login/get-otp",
    response_model=GenericResponse[UnverifiedUserDto],
    tags=["Driver Auth"],
)
@rest_endpoint
async def login_driver(
    request: LoginDriverDto, mediator: Annotated[Mediator, Depends(mediator)]
):
    LOG.info("Sending LoginDriverCommand to mediator with request: %s", request)
    return await mediator.send(LoginDriverCommand(dto=request))


@router.post(
    "/login/verify",
    response_model=GenericResponse[DriverAccountDto],
    tags=["Driver Auth"],
)
@rest_endpoint
async def login_driver_verify(
    request: LoginUserVerifyDto, mediator: Annotated[Mediator, Depends(mediator)]
):
    LOG.info("Sending LoginDriverVerifyCommand to mediator with request: %s", request)
    return await mediator.send(LoginDriverVerifyCommand(dto=request))


@router.get("/me", response_model=GenericResponse[DriverDto], tags=["Driver Features"])
@rest_endpoint
async def get_driver(
    mediator: Annotated[Mediator, Depends(mediator)],
    auth: Annotated[HTTPAuthorizationCredentials, Depends(oauth2_scheme)],
):
    LOG.info(
        "Sending GetDriverByUserIdQuery to mediator with user_id: %s", auth.credentials
    )
    return await mediator.send(GetDriverByUserIdQuery(user_id=auth.credentials))


@router.get(
    "/me/delivery_jobs",
    response_model=GenericResponse[list[DeliveryJobDto]],
    tags=["Driver Features"],
)
@rest_endpoint
async def get_driver_delivery_jobs(
    mediator: Annotated[Mediator, Depends(mediator)],
    auth: Annotated[HTTPAuthorizationCredentials, Depends(oauth2_scheme)],
):

    driver_id = await _get_driver_id(auth.credentials, mediator)
    LOG.info(
        "Sending GetDriverDeliveryJobsQuery to mediator with driver_id: %s", driver_id
    )
    return await mediator.send(GetDriverDeliveryJobsQuery(driver_id))


@router.get(
    "/me/orders",
    response_model=GenericResponse[list[OrderDto]],
    tags=["Driver Features"],
)
@rest_endpoint
async def get_driver_orders(
    mediator: Annotated[Mediator, Depends(mediator)],
    auth: Annotated[HTTPAuthorizationCredentials, Depends(oauth2_scheme)],
):

    driver_id = await _get_driver_id(auth.credentials, mediator)
    LOG.info("Sending GetDriverOrdersQuery to mediator with driver_id: %s", driver_id)
    return await mediator.send(GetDriverOrdersQuery(driver_id))


@router.get(
    "/me/payment/summary",
    response_model=GenericResponse[DriverPaymentSummaryDto],
    tags=["Driver Features"],
)
@rest_endpoint
async def get_driver_payment_summary(
    mediator: Annotated[Mediator, Depends(mediator)],
    auth: Annotated[HTTPAuthorizationCredentials, Depends(oauth2_scheme)],
):

    driver_id = await _get_driver_id(auth.credentials, mediator)
    LOG.info(
        "Sending GetDriverPaymentSummaryQuery to mediator with driver_id: %s", driver_id
    )
    return await mediator.send(GetDriverPaymentSummaryQuery(driver_id))


@router.get(
    "/me/payment/held-funds",
    response_model=GenericResponse[DriverHeldFundsDto],
    tags=["Driver Features"],
)
@rest_endpoint
async def get_driver_held_funds(
    mediator: Annotated[Mediator, Depends(mediator)],
    auth: Annotated[HTTPAuthorizationCredentials, Depends(oauth2_scheme)],
):

    driver_id = await _get_driver_id(auth.credentials, mediator)
    LOG.info(
        "Sending GetDriverHeldFundsQuery to mediator with driver_id: %s", driver_id
    )
    return await mediator.send(GetDriverHeldFundsQuery(driver_id))


@router.get(
    "/me/notifications",
    response_model=GenericResponse[list[NotificationDto]],
    tags=["Driver Features"],
)
@rest_endpoint
async def get_driver_notifications(
    mediator: Annotated[Mediator, Depends(mediator)],
    auth: Annotated[HTTPAuthorizationCredentials, Depends(oauth2_scheme)],
):

    # Notifications are user-scoped (user_id), not driver-scoped—hence no _get_driver_id call
    LOG.info(
        "Sending GetNotificationsQuery to mediator with user_id: %s", auth.credentials
    )
    return await mediator.send(GetNotificationsQuery(UUID(auth.credentials)))


@router.post(
    "/me/delivery_jobs/{delivery_job_id}/claim",
    response_model=GenericResponse[DeliveryJobDto],
    tags=["Driver Features"],
)
@rest_endpoint
async def claim_delivery_job(
    delivery_job_id: UUID,
    mediator: Annotated[Mediator, Depends(mediator)],
    auth: Annotated[HTTPAuthorizationCredentials, Depends(oauth2_scheme)],
):
    driver_id = await _get_driver_id(auth.credentials, mediator)
    return await mediator.send(
        ClaimDeliveryJobCommand(
            driver_id=driver_id,
            delivery_job_id=delivery_job_id,
        )
    )


@router.post(
    "/me/delivery_jobs/{delivery_job_id}/cancel",
    response_model=GenericResponse[DeliveryJobDto],
    tags=["Driver Features"],
)
@rest_endpoint
async def cancel_delivery_job(
    delivery_job_id: UUID,
    mediator: Annotated[Mediator, Depends(mediator)],
    auth: Annotated[HTTPAuthorizationCredentials, Depends(oauth2_scheme)],
):
    driver_id = await _get_driver_id(auth.credentials, mediator)
    LOG.info(
        "Sending CancelDeliveryJobCommand to mediator with driver_id: %s and delivery_job_id: %s",
        driver_id,
        delivery_job_id,
    )
    return await mediator.send(CancelDeliveryJobCommand(driver_id, delivery_job_id))


@router.post(
    "/me/delivery_jobs/{delivery_job_id}/orders/{order_id}/pick-up",
    response_model=GenericResponse[PickUpOrderDto],
    tags=["Driver Features"],
)
@rest_endpoint
async def initiate_order_pick_up(
    delivery_job_id: UUID,
    order_id: UUID,
    mediator: Annotated[Mediator, Depends(mediator)],
    auth: Annotated[HTTPAuthorizationCredentials, Depends(oauth2_scheme)],
):
    driver_id = await _get_driver_id(auth.credentials, mediator)
    LOG.info(
        "Sending PickUpOrderCommand to mediator with driver_id: %s, delivery_job_id: %s, and order_id: %s",
        driver_id,
        delivery_job_id,
        order_id,
    )
    return await mediator.send(PickUpOrderCommand(driver_id, delivery_job_id, order_id))


@router.post(
    "/me/delivery_jobs/{delivery_job_id}/orders/{order_id}/pick-up/verify",
    response_model=GenericResponse[None],
    tags=["Driver Features"],
)
@rest_endpoint
async def verify_order_pick_up(
    delivery_job_id: UUID,
    order_id: UUID,
    dto: PickUpOrderVerifyDto,
    mediator: Annotated[Mediator, Depends(mediator)],
    auth: Annotated[HTTPAuthorizationCredentials, Depends(oauth2_scheme)],
):
    driver_id = await _get_driver_id(auth.credentials, mediator)
    return await mediator.send(
        PickUpOrderVerifyCommand(driver_id, delivery_job_id, order_id, dto)
    )


@router.post(
    "/me/delivery_jobs/{delivery_job_id}/orders/{order_id}/drop-off",
    response_model=GenericResponse[DropOffOrderDto],
    tags=["Driver Features"],
)
@rest_endpoint
async def initiate_order_drop_off(
    delivery_job_id: UUID,
    order_id: UUID,
    mediator: Annotated[Mediator, Depends(mediator)],
    auth: Annotated[HTTPAuthorizationCredentials, Depends(oauth2_scheme)],
):
    driver_id = await _get_driver_id(auth.credentials, mediator)
    return await mediator.send(
        DropOffOrderCommand(driver_id, delivery_job_id, order_id)
    )


@router.post(
    "/me/delivery_jobs/{delivery_job_id}/orders/{order_id}/drop-off/verify",
    response_model=GenericResponse[None],
    tags=["Driver Features"],
)
@rest_endpoint
async def verify_order_drop_off(
    delivery_job_id: UUID,
    order_id: UUID,
    dto: DropOffOrderVerifyDto,
    mediator: Annotated[Mediator, Depends(mediator)],
    auth: Annotated[HTTPAuthorizationCredentials, Depends(oauth2_scheme)],
):
    driver_id = await _get_driver_id(auth.credentials, mediator)
    return await mediator.send(
        DropOffOrderVerifyCommand(driver_id, delivery_job_id, order_id, dto)
    )


async def _get_driver_id(user_id: str, mediator: Mediator) -> UUID:

    response = (await mediator.send(GetDriverByUserIdQuery(user_id=user_id))).to_dict()

    if (
        not response["is_success"]
        or "data" not in response
        or "id" not in response["data"]
    ):
        raise ApplicationException(
            Exceptions.NotFoundException,
            "Driver not found.",
            response.get("errors", ["Failed to retrieve driver."]),
        )

    return response["data"]["id"]


@router.websocket("/{driver_id}/location")
async def websocket_endpoint(
    driver_id: UUID,
    websocket: WebSocket,
    mediator: Annotated[Mediator, Depends(mediator)],
):
    await websocket.accept()

    while True:
        dto: UpdateLocationDto = await websocket.receive_json()
        LOG.info(
            "Sending UpdateDriverCurrentLocationCommand to mediator with driver_id: %s and dto: %s",
            driver_id,
            dto,
        )
        response = await mediator.send(
            UpdateDriverCurrentLocationCommand(driver_id, dto)
        )

        await websocket.send_json(response.to_dict())
