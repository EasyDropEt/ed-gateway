from ed_domain_model.services.auth.auth_endpoints import AuthEndpoint
from ed_domain_model.services.auth.dtos import (CreateUserDto,
                                                CreateUserVerifyDto,
                                                LoginUserDto,
                                                LoginUserVerifyDto,
                                                UnverifiedUserDto, UserDto,
                                                VerifyTokenDto)

from src.application.common.responses.api_response import ApiResponse
from src.application.contracts.infrastructure.api.abc_auth_api_handler import \
    ABCAuthApiHandler
from src.infrastructure.api.api_client import ApiClient


class AuthApiHandler(ABCAuthApiHandler):
    def __init__(self, auth_api: str) -> None:
        self._driver_endpoints = AuthEndpoint(auth_api)

    def create_get_otp(self, create_user_dto: CreateUserDto) -> ApiResponse[UnverifiedUserDto]:
        endpoint = self._driver_endpoints.get_description('create_get_otp')

        api_client = ApiClient[UnverifiedUserDto](endpoint)

        return api_client({'request': create_user_dto})

    def create_verify_otp(self, create_user_verify_dto: CreateUserVerifyDto) -> ApiResponse[UserDto]:
        endpoint = self._driver_endpoints.get_description('create_verify_otp')

        api_client = ApiClient[UserDto](endpoint)
        return api_client({'request': create_user_verify_dto}) 

    def login_get_otp(self, login_user_dto: LoginUserDto) -> ApiResponse[UnverifiedUserDto]:
        endpoint = self._driver_endpoints.get_description('login_get_otp')

        api_client = ApiClient[UnverifiedUserDto](endpoint)

        return api_client({'request': login_user_dto}) 

    def login_verify_otp(self, login_user_verify_dto: LoginUserVerifyDto) -> ApiResponse[UserDto]:
        endpoint = self._driver_endpoints.get_description('login_verify_otp')

        api_client = ApiClient[UserDto](endpoint)

        return api_client({'request': login_user_verify_dto}) 

    def verify_token(self, verify_token_dto: VerifyTokenDto) -> ApiResponse[UserDto]:
        endpoint = self._driver_endpoints.get_description('verify_token')

        api_client = ApiClient[UserDto](endpoint)

        return api_client({'request': verify_token_dto})
