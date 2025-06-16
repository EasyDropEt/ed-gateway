from dataclasses import dataclass

from ed_core.application.features.business.dtos.create_order_dto import \
    CreateParcelDto
from rmediator.decorators import request
from rmediator.mediator import Request

from ed_gateway.application.common.responses.base_response import BaseResponse
from ed_gateway.application.features.business.dtos import CheckoutDto


@request(BaseResponse[CheckoutDto])
@dataclass
class InitializeCheckoutCommand(Request):
    api_key: str
    callback_url: str
    parcel: CreateParcelDto
