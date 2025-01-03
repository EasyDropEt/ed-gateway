from datetime import datetime

from rmediator.decorators import request_handler
from rmediator.types import RequestHandler

from src.application.common.responses.base_response import BaseResponse
from src.application.contracts.infrastructure.persistence.abc_unit_of_work import (
    ABCUnitOfWork,
)
from src.application.features.drivers.dtos.delivery_job_dto import DeliveryJobDto
from src.application.features.drivers.requests.queries.get_delivery_job_by_id_query import (
    GetDeliveryJobByIdQuery,
)
from src.common.logging_helpers import get_logger
from src.domain.entities.order import OrderStatus, ParcelSize
from src.domain.entities.route import WayPointAction

LOG = get_logger()


@request_handler(GetDeliveryJobByIdQuery, BaseResponse[DeliveryJobDto])
class GetDeliveryJobByIdQueryHandler(RequestHandler):
    def __init__(self, uow: ABCUnitOfWork):
        self._uow = uow

    async def handle(
        self, request: GetDeliveryJobByIdQuery
    ) -> BaseResponse[DeliveryJobDto]:
        return BaseResponse[DeliveryJobDto].success(
            "Delivery job fetched successfully.",
            {
                "orders": [
                    {
                        "consumer": {
                            "name": "Shamil Bedru",
                            "phone_number": "string",
                            "email": "string",
                        },
                        "business": {
                            "business_name": "Queen Supermarket",
                            "owner_first_name": "Firaol",
                            "owner_last_name": "Ibrahim",
                            "email": "firaol.ibrahim@gmail.com",
                            "phone_number": "+251977346620",
                            "location": {
                                "address": "King George VI Street",
                                "latitude": 0,
                                "longitude": 0,
                                "postal_code": "0000",
                                "city": "Addis Ababa",
                            },
                        },
                        "latest_time_of_arrival": datetime.fromisoformat(
                            "2025-01-03T05:40:44.860Z"
                        ),
                        "parcel": {
                            "size": ParcelSize.SMALL,
                            "weight": 2,
                            "dimensions": {"length": 4, "width": 10, "height": 5},
                            "fragile": True,
                        },
                        "status": OrderStatus.PENDING,
                    }
                ],
                "route": {
                    "waypoints": [
                        {
                            "action": WayPointAction.PICKUP,
                            "eta": datetime.fromisoformat("2025-01-03T05:40:44.860Z"),
                            "sequence": 1,
                            "location": {
                                "address": "King George VI Street",
                                "latitude": 0,
                                "longitude": 0,
                                "postal_code": "0000",
                                "city": "Addis Ababa",
                            },
                        },
                        {
                            "action": WayPointAction.DROP_OFF,
                            "eta": datetime.fromisoformat("2025-01-03T05:40:44.860Z"),
                            "sequence": 2,
                            "location": {
                                "address": "King George VI Street",
                                "latitude": 0,
                                "longitude": 0,
                                "postal_code": "0000",
                                "city": "Addis Ababa",
                            },
                        },
                    ],
                    "estimated_distance_in_kms": 30.2,
                    "estimated_time_in_minutes": 102,
                },
                "estimated_payment": 0,
                "estimated_completion_time": datetime.fromisoformat(
                    "2025-01-03T05:40:44.860Z"
                ),
            },
        )
