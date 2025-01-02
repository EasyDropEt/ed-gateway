from uuid import UUID

from fastapi import APIRouter, Depends
from rmediator.decorators.request_handler import Annotated
from rmediator.mediator import Mediator

from src.application.features.business.dtos import (
    BusinessAccountDto,
    CreateBusinessAccountDto,
    CreateOrderDto,
    LoginBusinessDto,
    OrderDto,
)
from src.application.features.business.requests.commands import (
    CreateBusinessAccountCommand,
    CreateOrderCommand,
    LoginBusinessCommand,
)
from src.application.features.business.requests.queries import (
    GetOrderByIdQuery,
    GetOrdersQuery,
)
from src.common.logging_helpers import get_logger
from src.webapi.common.helpers import GenericResponse, rest_endpoint
from src.webapi.dependency_setup import mediator

LOG = get_logger()
router = APIRouter(prefix="/business", tags=["Business Feature"])


@router.post("/account/create", response_model=GenericResponse[BusinessAccountDto])
@rest_endpoint
async def create_account(mediator: Annotated[Mediator, Depends(mediator)]):
    return await mediator.send(
        CreateBusinessAccountCommand(dto=CreateBusinessAccountDto())
    )


@router.post("/account/login", response_model=GenericResponse[BusinessAccountDto])
@rest_endpoint
async def login(mediator: Annotated[Mediator, Depends(mediator)]):
    return await mediator.send(LoginBusinessCommand(dto=LoginBusinessDto()))


@router.get("/orders/{business_id}", response_model=GenericResponse[list[OrderDto]])
@rest_endpoint
async def get_orders(
    business_id: UUID,
    mediator: Annotated[Mediator, Depends(mediator)],
):
    return await mediator.send(GetOrdersQuery(business_id=business_id))


@router.get("/orders/{order_id}", response_model=GenericResponse[OrderDto])
@rest_endpoint
async def get_order_by_id(
    order_id: UUID, mediator: Annotated[Mediator, Depends(mediator)]
):
    return await mediator.send(GetOrderByIdQuery(order_id=order_id))


@router.post("/orders", response_model=GenericResponse[OrderDto])
@rest_endpoint
async def create_order(
    create_order_dto: CreateOrderDto, mediator: Annotated[Mediator, Depends(mediator)]
):
    return await mediator.send(CreateOrderCommand(dto=create_order_dto))
