import urllib.parse

from ed_core.application.features.business.dtos.create_order_dto import \
    CreateParcelDto
from ed_domain.common.exceptions import EXCEPTION_NAMES, ApplicationException
from rmediator.decorators import request_handler
from rmediator.types import RequestHandler

from ed_gateway.application.common.responses.base_response import BaseResponse
from ed_gateway.application.contracts.infrastructure.api.abc_api import ABCApi
from ed_gateway.application.features.business.dtos.checkout_dto import \
    CheckoutDto
from ed_gateway.application.features.business.requests.commands import \
    InitializeCheckoutCommand
from ed_gateway.common.logging_helpers import get_logger

LOG = get_logger()


@request_handler(InitializeCheckoutCommand, BaseResponse[CheckoutDto])
class InitializeCheckoutCommandHandler(RequestHandler):
    def __init__(self, api: ABCApi):
        self._api = api

        self._error_message = "Order checkout cannot be initialized."
        self._success_message = "Order checkout initialized succesfully."

    async def handle(
        self, request: InitializeCheckoutCommand
    ) -> BaseResponse[CheckoutDto]:
        LOG.info("Calling core verify_api_key API")
        response = await self._api.core_api.verify_api_key(request.api_key)

        LOG.info(f"Received response from get_business_api_keys: {response}")
        if response["is_success"] is False:
            raise ApplicationException(
                EXCEPTION_NAMES[response["http_status_code"]],
                self._error_message,
                response["errors"],
            )

        business = response["data"]
        api_key_response = await self._api.core_api.create_business_api_key(
            str(business["id"]),
            {
                "name": "Temporary API key created by system",
                "description": "Ignore this.",
            },
        )

        key = api_key_response["data"]["key"]
        assert key is not None

        base_url = "https://base.url"
        return BaseResponse[CheckoutDto].success(
            self._success_message,
            CheckoutDto(
                url=self.build_checkout_url(
                    api_key=key,
                    business_name=business["business_name"],
                    base_url=base_url,
                    parcel=request.parcel,
                    call_back_url=request.callback_url,
                )
            ),
        )

    def build_checkout_url(
        self,
        api_key: str,
        business_name: str,
        base_url: str,
        parcel: CreateParcelDto,
        call_back_url: str,
    ) -> str:
        query_data = {
            "size": parcel["size"].value,
            "length": parcel["length"],
            "width": parcel["width"],
            "height": parcel["height"],
            "weight": parcel["weight"],
            "fragile": int(parcel["fragile"]),
            "callback_url": call_back_url,
            "business_name": business_name,
        }
        query_string = urllib.parse.urlencode(query_data)
        separator = "&" if "?" in base_url else "?"
        checkout_url = f"{base_url}{separator}api_key={api_key}&{query_string}"
        return checkout_url
