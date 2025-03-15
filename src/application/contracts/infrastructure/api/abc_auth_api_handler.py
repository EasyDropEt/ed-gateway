from abc import ABCMeta, abstractmethod

from ed_domain_model.services.auth.dtos import (CreateUserDto,
                                                CreateUserVerifyDto,
                                                LoginUserDto,
                                                LoginUserVerifyDto,
                                                UnverifiedUserDto, UserDto,
                                                VerifyTokenDto)


class ABCAuthApiHandler(metaclass=ABCMeta):
    @abstractmethod
    def create_get_otp(self, create_user_dto: CreateUserDto) -> UnverifiedUserDto: ...

    @abstractmethod
    def create_verify_otp(self, create_user_verify_dto: CreateUserVerifyDto) -> UserDto: ...

    @abstractmethod
    def login_get_otp(self, login_user_dto: LoginUserDto) -> UnverifiedUserDto: ...

    @abstractmethod
    def login_verify_otp(self, login_user_verify_dto: LoginUserVerifyDto) -> UserDto: ...

    @abstractmethod
    def verify_token(self, verify_token_dto: VerifyTokenDto) -> UserDto: ...
