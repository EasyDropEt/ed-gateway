from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, WebSocket
from rmediator import Mediator

from src.application.features.drivers.dtos import (
    CreateDriverAccountDto,
    DeliveryJobDto,
    DriverAccountDto,
    LoginDriverDto,
)
from src.application.features.drivers.requests.commands import (
    CreateDriverAccountCommand,
    LoginDriverCommand,
)
from src.application.features.drivers.requests.queries import (
    GetDeliveryJobByIdQuery,
    GetDeliveryJobsQuery,
)
from src.common.logging_helpers import get_logger
from src.webapi.common.helpers import GenericResponse, rest_endpoint
from src.webapi.dependency_setup import mediator

LOG = get_logger()
router = APIRouter(prefix="/drivers", tags=["Driver Features"])


@router.get("/delivery-jobs", response_model=GenericResponse[list[DeliveryJobDto]])
@rest_endpoint
async def available_jobs(mediator: Annotated[Mediator, Depends(mediator)]):
    return await mediator.send(GetDeliveryJobsQuery())


@router.get("/delivery-jobs/{job_id}", response_model=GenericResponse[DeliveryJobDto])
@rest_endpoint
async def available_job_by_id(
    job_id: UUID, mediator: Annotated[Mediator, Depends(mediator)]
):
    return await mediator.send(GetDeliveryJobByIdQuery(id=job_id))


@router.websocket("/delivery-jobs/{job_id}/route")
async def websocket(ws: WebSocket) -> None:
    await ws.accept()

    while True:
        data = await ws.receive_text()
        await ws.send_text(f"Message text was: {data}")


@router.post("/account/create", response_model=GenericResponse[DriverAccountDto])
@rest_endpoint
async def create_account(mediator: Annotated[Mediator, Depends(mediator)]):
    return await mediator.send(CreateDriverAccountCommand(dto=CreateDriverAccountDto()))


@router.post("/account/login", response_model=GenericResponse[DriverAccountDto])
@rest_endpoint
async def login(mediator: Annotated[Mediator, Depends(mediator)]):
    return await mediator.send(LoginDriverCommand(dto=LoginDriverDto()))
