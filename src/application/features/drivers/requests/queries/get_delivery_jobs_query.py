from dataclasses import dataclass

from rmediator.decorators import request
from rmediator.mediator import Request

from src.application.common.responses.base_response import BaseResponse
from src.application.features.drivers.dtos.delivery_job_dto import DeliveryJobDto


@request(BaseResponse[list[DeliveryJobDto]])
@dataclass
class GetDeliveryJobsQuery(Request): ...
