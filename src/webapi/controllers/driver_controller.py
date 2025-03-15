from typing import Annotated

from ed_domain_model.services.auth.dtos import (LoginUserVerifyDto,
                                                UnverifiedUserDto)
from ed_domain_model.services.core.dtos.driver_dto import DriverDto
from fastapi import APIRouter, Depends
from rmediator import Mediator

from src.application.features.drivers.dtos import (CreateDriverAccountDto,
                                                   DriverAccountDto)
from src.application.features.drivers.dtos.login_driver_dto import \
    LoginDriverDto
from src.application.features.drivers.requests.commands.create_driver_account_command import \
    CreateDriverAccountCommand
from src.application.features.drivers.requests.commands.login_driver_command import \
    LoginDriverCommand
from src.application.features.drivers.requests.commands.login_driver_verify_command import \
    LoginDriverVerifyCommand
from src.common.logging_helpers import get_logger
from src.webapi.common.helpers import GenericResponse, rest_endpoint
from src.webapi.dependency_setup import mediator

LOG = get_logger()
router = APIRouter(prefix="/drivers", tags=["Driver Features"])

@router.post("", response_model=GenericResponse[DriverAccountDto])
@rest_endpoint
async def create_account(request: CreateDriverAccountDto, mediator: Annotated[Mediator, Depends(mediator)]):
    return await mediator.send(CreateDriverAccountCommand(dto=request))

@router.post("/login/get-otp", response_model=GenericResponse[UnverifiedUserDto])
@rest_endpoint
async def login_driver(request: LoginDriverDto, mediator: Annotated[Mediator, Depends(mediator)]):
    return await mediator.send(LoginDriverCommand(dto=request))

@router.post("/login/verify", response_model=GenericResponse[DriverDto])
@rest_endpoint
async def login_driver_verify(request: LoginUserVerifyDto, mediator: Annotated[Mediator, Depends(mediator)]):
    return await mediator.send(LoginDriverVerifyCommand(dto=request))
