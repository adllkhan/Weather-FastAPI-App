from fastapi import APIRouter, HTTPException, status

from ..services import WeatherServices as Services
from ..services import AuthServices


router = APIRouter(prefix="/weather", tags=["Weather API"])
services = Services()


@router.get(
    path="",
    description="Get weather by city or coordinates by OpenWeatherMap API",
    responses={
        status.HTTP_200_OK: {
            "description": "Get weather by city or coordinates",
            "content": {
                "application/json": {
                    "example": {
                        "city": "string",
                        "temperature": 0.0,
                        "description": "string",
                    }
                }
            },
        },
        status.HTTP_400_BAD_REQUEST: {
            "description": "Invalid query parameters",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Invalid query parameters"
                    }
                }
            },
        },
    }
)
async def get_weather(
    access_token: str,
    city: str | None = None,
    lat: float | None = None,
    lon: float | None = None,
    units: str = "metric",
    lang: str = "en",
):
    user = await AuthServices().get_user(token=access_token)
    if city:
        return await services.get_weather_by_city(
            city=city,
            units=units,
            lang=lang,
            user=user
        )
    elif lat and lon:
        return await services.get_weather_by_coordinates(
            user=user,
            lat=lat,
            lon=lon,
            units=units,
            lang=lang
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid query parameters"
        )
