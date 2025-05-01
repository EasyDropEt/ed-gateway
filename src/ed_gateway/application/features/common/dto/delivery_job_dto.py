from datetime import datetime
from typing import TypedDict

from ed_gateway.domain.entities.order import OrderStatus, Parcel
from ed_gateway.domain.entities.route import WayPointAction


class LocationDto(TypedDict):
    address: str
    latitude: float
    longitude: float
    postal_code: str
    city: str


class BusinessDto(TypedDict):
    business_name: str
    owner_first_name: str
    owner_last_name: str
    email: str
    phone_number: str
    location: LocationDto


class ConsumerDto(TypedDict):
    name: str
    phone_number: str
    email: str


class OrderDto(TypedDict):
    consumer: ConsumerDto
    business: BusinessDto
    parcel: Parcel
    status: OrderStatus
    latest_time_of_arrival: datetime


class WayPointDto(TypedDict):
    action: WayPointAction
    eta: datetime
    sequence: int
    location: LocationDto


class RouteDto(TypedDict):
    waypoints: list[WayPointDto]
    estimated_distance_in_kms: float
    estimated_time_in_minutes: int


class DeliveryJobDto(TypedDict):
    orders: list[OrderDto]
    route: RouteDto
    estimated_payment: float
    estimated_completion_time: datetime
