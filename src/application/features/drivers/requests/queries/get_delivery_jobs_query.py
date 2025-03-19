from dataclasses import dataclass

from ed_domain_model.services.core.dtos import DeliveryJobDto
from rmediator.decorators import request
from rmediator.mediator import Request

from src.application.common.responses.base_response import BaseResponse


@request(BaseResponse[list[DeliveryJobDto]])
@dataclass
class GetDeliveryJobsQuery(Request):
    ...
