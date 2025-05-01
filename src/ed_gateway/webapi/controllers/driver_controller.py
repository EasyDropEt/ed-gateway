from typing import Annotated
from uuid import UUID

from ed_auth.application.features.auth.dtos import (LoginUserVerifyDto,
                                                    UnverifiedUserDto)
from ed_core.documentation.abc_core_api_client import DriverDto
from fastapi import APIRouter, Depends
from rmediator import Mediator

from ed_gateway.application.features.drivers.dtos import (
    CreateDriverAccountDto, DriverAccountDto, LoginDriverDto)
from ed_gateway.application.features.drivers.requests.commands import (
    CreateDriverAccountCommand, LoginDriverCommand, LoginDriverVerifyCommand)
from ed_gateway.application.features.drivers.requests.queries import (
    GetDriverByIdQuery, GetDriverDeliveryJobsQuery)
from ed_gateway.common.logging_helpers import get_logger
from ed_gateway.webapi.common.helpers import GenericResponse, rest_endpoint
from ed_gateway.webapi.dependency_setup import mediator

LOG = get_logger()
router = APIRouter(prefix="/drivers", tags=["Driver Features"])


@router.post("", response_model=GenericResponse[DriverAccountDto])
@rest_endpoint
async def create_account(
    request: CreateDriverAccountDto, mediator: Annotated[Mediator, Depends(mediator)]
):
    return await mediator.send(CreateDriverAccountCommand(dto=request))


@router.post("/login/get-otp", response_model=GenericResponse[UnverifiedUserDto])
@rest_endpoint
async def login_driver(
    request: LoginDriverDto, mediator: Annotated[Mediator, Depends(mediator)]
):
    return await mediator.send(LoginDriverCommand(dto=request))


@router.post("/login/verify", response_model=GenericResponse[DriverDto])
@rest_endpoint
async def login_driver_verify(
    request: LoginUserVerifyDto, mediator: Annotated[Mediator, Depends(mediator)]
):
    return await mediator.send(LoginDriverVerifyCommand(dto=request))


@router.get("/{driver_id}", response_model=GenericResponse[DriverDto])
@rest_endpoint
async def get_driver(driver_id: UUID, mediator: Annotated[Mediator, Depends(mediator)]):
    return await mediator.send(GetDriverByIdQuery(driver_id=driver_id))


@router.get("/{driver_id}/delivery_jobs", response_model=GenericResponse[DriverDto])
@rest_endpoint
async def get_driver_delivery_jobs(
    driver_id: UUID, mediator: Annotated[Mediator, Depends(mediator)]
):
    return await mediator.send(GetDriverDeliveryJobsQuery(driver_id=driver_id))
