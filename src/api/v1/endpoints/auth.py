from fastapi import APIRouter, status

from ..services import AuthServices as Services
from ..schemas import UserOut, UserIn, Token
from ..core import (
    InvalidCredentialsException,
    UserExistsException,
)


router = APIRouter(prefix="/auth", tags=["Authentication"])
services = Services()


@router.post(
    "/login",
    response_model=Token,
    description="Returns access-token",
    responses={
        status.HTTP_200_OK: {
            "access_token": "string",
            "token_type": "string",
        },
        InvalidCredentialsException().status_code: {
            "detail": InvalidCredentialsException().detail
        },
    },
)
async def login(user: UserIn) -> Token:
    return await services.login(user=user)


@router.post(
    "/register",
    response_model=UserOut,
    description="Register a new user",
    responses={
        status.HTTP_200_OK: {
            "username": "string",
        },
        UserExistsException().status_code: {
            "detail": UserExistsException().detail
        },
    },
)
async def register(user: UserIn) -> UserOut:
    return await services.register(user=user)
