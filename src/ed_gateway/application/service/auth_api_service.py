from ed_auth.documentation.api.abc_auth_api_client import (ABCAuthApiClient,
                                                           CreateOrGetUserDto,
                                                           CreateUserDto,
                                                           CreateUserVerifyDto,
                                                           LoginUserDto,
                                                           LoginUserVerifyDto,
                                                           UnverifiedUserDto,
                                                           UserDto)
from ed_domain.common.exceptions import EXCEPTION_NAMES, ApplicationException
from ed_domain.common.logging import get_logger

LOG = get_logger()


class AuthApiService:
    def __init__(self, api: ABCAuthApiClient) -> None:
        self._api = api

    async def create_or_get(self, dto: CreateUserDto) -> CreateOrGetUserDto:
        LOG.info(f"Calling auth create_get_otp API with request: {dto}")
        response = await self._api.create_or_get_user(dto)

        LOG.info(
            "Received response from create_get_otp - success: %s",
            response.get("is_success"),
        )
        if not response["is_success"]:
            raise ApplicationException(
                EXCEPTION_NAMES[response["http_status_code"]],
                "User was not created.",
                response["errors"],
            )

        return response["data"]

    async def create(self, dto: CreateUserDto) -> UnverifiedUserDto:
        LOG.info(f"Calling auth create_get_otp API with request: {dto}")
        response = await self._api.create_get_otp(dto)

        LOG.info(
            "Received response from create_get_otp - success: %s",
            response.get("is_success"),
        )
        if not response["is_success"]:
            raise ApplicationException(
                EXCEPTION_NAMES[response["http_status_code"]],
                "User was not created.",
                response["errors"],
            )

        return response["data"]

    async def create_verify(self, dto: CreateUserVerifyDto) -> UserDto:
        LOG.info(f"Calling auth create_get_otp API with request: {dto}")
        response = await self._api.create_verify_otp(dto)

        LOG.info(
            "Received response from create_get_otp - success: %s",
            response.get("is_success"),
        )
        if not response["is_success"]:
            raise ApplicationException(
                EXCEPTION_NAMES[response["http_status_code"]],
                "User was not created.",
                response["errors"],
            )

        return response["data"]

    async def login(self, dto: LoginUserDto) -> UnverifiedUserDto:
        LOG.info(f"Calling auth login_get_otp API with request: {dto}")
        response = await self._api.login_get_otp(dto)

        LOG.info(f"Received response from login_get_otp: {response}")
        if not response["is_success"]:
            raise ApplicationException(
                EXCEPTION_NAMES[response["http_status_code"]],
                "Failed to send OTP for log-in",
                response["errors"],
            )

        return response["data"]

    async def login_verify(self, dto: LoginUserVerifyDto) -> UserDto:
        LOG.info(f"Calling auth login_get_otp API with request: {dto}")
        response = await self._api.login_verify_otp(dto)

        LOG.info(f"Received response from login_get_otp: {response}")
        if not response["is_success"]:
            raise ApplicationException(
                EXCEPTION_NAMES[response["http_status_code"]],
                "Failed to send OTP for log-in",
                response["errors"],
            )

        return response["data"]
