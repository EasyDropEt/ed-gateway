from typing import Annotated

from ed_auth.application.features.auth.dtos import (LoginUserVerifyDto,
                                                    UnverifiedUserDto)
from ed_core.documentation.abc_core_api_client import BusinessDto
from fastapi import APIRouter, Depends
from rmediator import Mediator

from ed_gateway.application.features.business.dtos import (
    BusinessAccountDto, CreateBusinessAccountDto, LoginBusinessDto)
from ed_gateway.application.features.business.requests.commands import (
    CreateBusinessAccountCommand, LoginBusinessCommand,
    LoginBusinessVerifyCommand)
from ed_gateway.common.logging_helpers import get_logger
from ed_gateway.webapi.common.helpers import GenericResponse, rest_endpoint
from ed_gateway.webapi.dependency_setup import mediator

LOG = get_logger()
router = APIRouter(prefix="/business", tags=["Business Features"])


@router.post("", response_model=GenericResponse[BusinessAccountDto])
@rest_endpoint
async def create_account(
    request: CreateBusinessAccountDto, mediator: Annotated[Mediator, Depends(mediator)]
):
    return await mediator.send(CreateBusinessAccountCommand(dto=request))


@router.post("/login/get-otp", response_model=GenericResponse[UnverifiedUserDto])
@rest_endpoint
async def login_driver(
    request: LoginBusinessDto, mediator: Annotated[Mediator, Depends(mediator)]
):
    return await mediator.send(LoginBusinessCommand(dto=request))


@router.post("/login/verify", response_model=GenericResponse[BusinessDto])
@rest_endpoint
async def login_driver_verify(
    request: LoginUserVerifyDto, mediator: Annotated[Mediator, Depends(mediator)]
):
    return await mediator.send(LoginBusinessVerifyCommand(dto=request))
