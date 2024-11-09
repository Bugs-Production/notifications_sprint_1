from enum import Enum

from core.config import settings
from fastapi import HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt
from jose.exceptions import ExpiredSignatureError, JWTError
from pydantic import BaseModel, ValidationError


class ServiceEnum(Enum):
    AUTH = "auth"
    UGC = "ugc"


ALLOWED_SERVICES = [ServiceEnum.AUTH.value, ServiceEnum.UGC.value]


class AccessTokenPayload(BaseModel):
    service_name: str
    iat: int
    exp: int


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> AccessTokenPayload:
        credentials: HTTPAuthorizationCredentials = await super().__call__(request)
        if not credentials:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid authorization code.",
            )
        if credentials.scheme != "Bearer":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Only Bearer token might be accepted",
            )

        return self.decode_and_parse_token(credentials.credentials)

    @staticmethod
    def decode_and_parse_token(jwt_token: str) -> AccessTokenPayload | None:
        try:
            decoded_token = jwt.decode(
                jwt_token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm]
            )
        except ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Access token is expired",
            )
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid format for JWT token",
            )
        try:
            access_token = AccessTokenPayload(**decoded_token)
        except ValidationError as exc:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Access token is invalid: {exc}",
            )
        return access_token


security_jwt = JWTBearer()


def check_token(access_token: AccessTokenPayload):
    if access_token.service_name not in ALLOWED_SERVICES:

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Service doesn't have required permissions",
        )
