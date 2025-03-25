from datetime import datetime

from ed_domain_model.services.core.dtos import DeliveryJobDto
from rmediator.decorators import request_handler
from rmediator.types import RequestHandler

from ed_gateway.application.common.responses.base_response import BaseResponse
from ed_gateway.application.contracts.infrastructure.api.abc_api import ABCApi
from ed_gateway.application.features.drivers.requests.queries.get_delivery_jobs_query import (
    GetDeliveryJobsQuery,
)
from ed_gateway.common.logging_helpers import get_logger
from ed_gateway.domain.entities.order import OrderStatus, ParcelSize
from ed_gateway.domain.entities.route import WayPointAction

LOG = get_logger()


@request_handler(GetDeliveryJobsQuery, BaseResponse[list[DeliveryJobDto]])
class GetDeliveryJobsQueryHandler(RequestHandler):
    def __init__(self, api: ABCApi):
        self._api = api

    async def handle(
        self, request: GetDeliveryJobsQuery
    ) -> BaseResponse[list[DeliveryJobDto]]:
        return BaseResponse[list[DeliveryJobDto]].success(
            "Delivery jobs fetched successfully.",
            [
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
                                "eta": datetime.fromisoformat(
                                    "2025-01-03T05:40:44.860Z"
                                ),
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
                                "eta": datetime.fromisoformat(
                                    "2025-01-03T05:40:44.860Z"
                                ),
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
                {
                    "orders": [
                        {
                            "consumer": {
                                "name": "Fikernew Birhanu",
                                "phone_number": "+251930306620",
                                "email": "string",
                            },
                            "business": {
                                "business_name": "Queen Supermarket",
                                "owner_first_name": "Firaol",
                                "owner_last_name": "Ibrahim",
                                "email": "firaol.ibrahim@gmail.com",
                                "phone_number": "+251977776620",
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
                                "eta": datetime.fromisoformat(
                                    "2025-01-03T05:40:44.860Z"
                                ),
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
                                "eta": datetime.fromisoformat(
                                    "2025-01-03T05:40:44.860Z"
                                ),
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
            ],
        )
