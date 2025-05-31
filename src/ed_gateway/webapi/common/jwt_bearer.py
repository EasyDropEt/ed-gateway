from ed_auth.documentation.api.auth_api_client import ABCAuthApiClient
from ed_domain.common.exceptions import ApplicationException, Exceptions
from fastapi import Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer


class JWTBearer(HTTPBearer):
    def __init__(self, api: ABCAuthApiClient, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)
        self._api = api

    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials:
        credentials: HTTPAuthorizationCredentials | None = await super(
            JWTBearer, self
        ).__call__(request)

        if not credentials:
            raise ApplicationException(
                Exceptions.UnauthorizedException,
                "Internal server error.",
                ["Authorization code not found."],
            )

        if not credentials.scheme == "Bearer":
            raise ApplicationException(
                Exceptions.UnauthorizedException,
                "Invalid authorization code.",
                ["Provide a Bearer token."],
            )

        response = self._api.verify_token({"token": credentials.credentials})
        if not response["is_success"]:
            raise ApplicationException(
                Exceptions.UnauthorizedException,
                "Invalid authorization token.",
                response["errors"],
            )

        return HTTPAuthorizationCredentials(
            scheme=credentials.scheme,
            credentials=str(response["data"]["id"]),
        )

    async def verify_token(self, token: str) -> HTTPAuthorizationCredentials:
        response = self._api.verify_token({"token": token})
        if not response["is_success"]:
            raise ApplicationException(
                Exceptions.UnauthorizedException,
                "Invalid authorization token.",
                response["errors"],
            )

        return HTTPAuthorizationCredentials(
            scheme="Bearer",
            credentials=str(response["data"]["id"]),
        )
