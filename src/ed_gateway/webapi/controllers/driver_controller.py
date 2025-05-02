from typing import Annotated
from uuid import UUID

from ed_auth.application.features.auth.dtos import (LoginUserVerifyDto,
                                                    UnverifiedUserDto)
from ed_core.documentation.abc_core_api_client import DeliveryJobDto, DriverDto
from fastapi import APIRouter, Depends
from fastapi.security import HTTPAuthorizationCredentials
from rmediator import Mediator

from ed_gateway.application.features.drivers.dtos import (
    CreateDriverAccountDto, DriverAccountDto, LoginDriverDto)
from ed_gateway.application.features.drivers.requests.commands import (
    ClaimDeliveryJobCommand, CreateDriverAccountCommand, LoginDriverCommand,
    LoginDriverVerifyCommand)
from ed_gateway.application.features.drivers.requests.queries import (
    GetDriverByUserIdQuery, GetDriverDeliveryJobsQuery)
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
    request: CreateDriverAccountDto, mediator: Annotated[Mediator, Depends(mediator)]
):
    return await mediator.send(CreateDriverAccountCommand(dto=request))


@router.post(
    "/login/get-otp",
    response_model=GenericResponse[UnverifiedUserDto],
    tags=["Driver Auth"],
)
@rest_endpoint
async def login_driver(
    request: LoginDriverDto, mediator: Annotated[Mediator, Depends(mediator)]
):
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
    return await mediator.send(LoginDriverVerifyCommand(dto=request))


@router.get("/me", response_model=GenericResponse[DriverDto], tags=["Driver Features"])
@rest_endpoint
async def get_driver(
    mediator: Annotated[Mediator, Depends(mediator)],
    auth: Annotated[HTTPAuthorizationCredentials, Depends(oauth2_scheme)],
):
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
    driver = (await mediator.send(GetDriverByUserIdQuery(user_id=auth.credentials)))[
        "data"
    ]
    print(driver)
    return await mediator.send(GetDriverDeliveryJobsQuery(driver_id=driver["id"]))


@router.post(
    "/me/delivery_jobs/{delivery_job_id}/claim",
    response_model=GenericResponse[list[DeliveryJobDto]],
    tags=["Driver Features"],
)
@rest_endpoint
async def claim_delivery_job(
    delivery_job_id: UUID,
    mediator: Annotated[Mediator, Depends(mediator)],
    auth: Annotated[HTTPAuthorizationCredentials, Depends(oauth2_scheme)],
):
    driver = (await mediator.send(GetDriverByUserIdQuery(user_id=auth.credentials)))[
        "data"
    ]
    print(driver)
    return await mediator.send(
        ClaimDeliveryJobCommand(
            driver_id=driver["id"], delivery_job_id=delivery_job_id)
    )
