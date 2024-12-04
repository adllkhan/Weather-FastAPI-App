from fastapi import APIRouter
from ..schemas import Histories
from ..core import (
    NotFoundException,
)
from ..services import HistoryServices, AuthServices


router = APIRouter(prefix="/history", tags=["History"])


@router.get(
    "",
    response_model=Histories,
    description="Get all user's history",
    responses={
        200: {
            "description": "Get all history",
            "content": {"application/json": {"example": []}},
        },
        NotFoundException().status_code: {
            "description": "Not found",
            "content": {
                "application/json": {
                    "example": {
                        "detail": NotFoundException().detail
                    }
                }
            },
        },
    }
)
async def get(access_token: str) -> Histories:
    user = await AuthServices().get_user(access_token)
    return await HistoryServices().get(user.id)
