from typing import Annotated

from ed_core.documentation.core_api_client import DeliveryJobDto
from fastapi import APIRouter, Depends
from rmediator import Mediator

from ed_gateway.application.features.delivery_jobs.requests.queries import \
    GetDeliveryJobsQuery
from ed_gateway.common.logging_helpers import get_logger
from ed_gateway.webapi.common.helpers import GenericResponse, rest_endpoint
from ed_gateway.webapi.dependency_setup import mediator

LOG = get_logger()
router = APIRouter(prefix="/delivery_job", tags=["Delivery Job Features"])


@router.get("", response_model=GenericResponse[list[DeliveryJobDto]])
@rest_endpoint
async def get_delivery_jobs(mediator: Annotated[Mediator, Depends(mediator)]):
    return await mediator.send(GetDeliveryJobsQuery())
