from ed_domain_model.services.auth.auth_endpoints import AuthEndpoint
from ed_domain_model.services.auth.dtos import (CreateUserDto,
                                                CreateUserVerifyDto,
                                                LoginUserDto,
                                                LoginUserVerifyDto,
                                                UnverifiedUserDto, UserDto,
                                                VerifyTokenDto)

from src.application.contracts.infrastructure.api.abc_auth_api_handler import \
    ABCAuthApiHandler
from src.infrastructure.api.api_client import ApiClient


class AuthApiHandler(ABCAuthApiHandler):
    def __init__(self, auth_api: str) -> None:
        self._driver_endpoints = AuthEndpoint(auth_api)

    def create_get_otp(self, create_user_dto: CreateUserDto) -> UnverifiedUserDto:
        endpoint = self._driver_endpoints.get_description('create_get_otp')

        api_client = ApiClient(endpoint)

        return api_client.send({'request': create_user_dto}) # type: ignore

    def create_verify_otp(self, create_user_verify_dto: CreateUserVerifyDto) -> UserDto:
        endpoint = self._driver_endpoints.get_description('create_verify_otp')

        api_client = ApiClient(endpoint)

        return api_client.send({'request': create_user_verify_dto}) # type: ignore

    def login_get_otp(self, login_user_dto: LoginUserDto) -> UnverifiedUserDto:
        endpoint = self._driver_endpoints.get_description('login_get_otp')

        api_client = ApiClient(endpoint)

        return api_client.send({'request': login_user_dto}) # type: ignore

    def login_verify_otp(self, login_user_verify_dto: LoginUserVerifyDto) -> UserDto:
        endpoint = self._driver_endpoints.get_description('login_verify_otp')

        api_client = ApiClient(endpoint)

        return api_client.send({'request': login_user_verify_dto}) # type: ignore

    def verify_token(self, verify_token_dto: VerifyTokenDto) -> UserDto:
        endpoint = self._driver_endpoints.get_description('verify_token')

        api_client = ApiClient(endpoint)

        return api_client.send({'request': verify_token_dto}) # type: ignore
