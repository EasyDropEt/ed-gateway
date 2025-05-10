from typing import Annotated
from uuid import UUID

from ed_core.application.features.common.dtos import TrackOrderDto
from fastapi import APIRouter, Depends
from rmediator import Mediator

from ed_gateway.application.features.order.requests.queries import \
    TrackOrderQuery
from ed_gateway.common.generic_helpers import get_config
from ed_gateway.common.logging_helpers import get_logger
from ed_gateway.webapi.common.helpers import GenericResponse, rest_endpoint
from ed_gateway.webapi.common.jwt_bearer import JWTBearer
from ed_gateway.webapi.dependency_setup import api as get_api
from ed_gateway.webapi.dependency_setup import mediator

LOG = get_logger()
router = APIRouter(prefix="/orders")
config = get_config()
api_dep = get_api(config)
oauth2_scheme = JWTBearer(api_dep.auth_api)


@router.get(
    "/{order_id}/track",
    response_model=GenericResponse[TrackOrderDto],
    tags=["Order Features"],
)
@rest_endpoint
async def get_driver(
    order_id: UUID,
    mediator: Annotated[Mediator, Depends(mediator)],
):
    return await mediator.send(TrackOrderQuery(order_id=order_id))
