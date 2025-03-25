from typing import Annotated

from ed_domain_model.services.auth.dtos import LoginUserVerifyDto, UnverifiedUserDto
from ed_domain_model.services.core.dtos.driver_dto import DriverDto
from fastapi import APIRouter, Depends
from rmediator import Mediator

from ed_gateway.application.features.drivers.dtos import (
    CreateDriverAccountDto,
    DriverAccountDto,
    LoginDriverDto,
)
from ed_gateway.application.features.drivers.requests.commands import (
    CreateDriverAccountCommand,
    LoginDriverCommand,
    LoginDriverVerifyCommand,
)
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
