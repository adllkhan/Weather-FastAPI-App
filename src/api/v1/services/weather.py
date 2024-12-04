from aiohttp import ClientSession
from fastapi import HTTPException

from .history import Services as HistoryServices
from ..core import Config
from ..repositories import UsersRepositories
from ..schemas import UserOut
from ..schemas import History as HistorySchema


class Services:
    def __init__(self):
        self.config = Config()
        self.users = UsersRepositories()
        self.history = HistoryServices()

    async def _save_history(
        self, response: dict, user: UserOut, city: bool
    ) -> HistorySchema:
        user = await self.users.get(_id=user.id)
        if city:
            history = HistorySchema(
                city=response["name"],
                temperature=response["main"]["temp"],
                description=response["weather"][0]["description"],
            )
        else:
            history = HistorySchema(
                longitude=response["coord"]["lon"],
                latitude=response["coord"]["lat"],
                temperature=response["main"]["temp"],
                description=response["weather"][0]["description"],
            )
        return await self.history.create(
            history=history,
            user_id=user.id
        )

    async def get_weather_by_city(
        self,
        city: str,
        user: UserOut,
        units: str = "metric",
        lang: str = "en",
    ) -> dict:
        params = {
            "q": city,
            "appid": self.config.WEATHER_API_KEY,
            "units": units,
            "lang": lang,
        }
        async with ClientSession() as session:
            async with session.get(
                url=self.config.WEATHER_API, params=params
            ) as response:
                if response.status != 200:
                    raise HTTPException(
                        status_code=response.status,
                        detail=await response.text()
                    )
                response = await response.json()
                await self._save_history(
                    response=response, user=user, city=True
                )
                return response

    async def get_weather_by_coordinates(
        self,
        lat: float,
        lon: float,
        user: UserOut,
        units: str = "metric",
        lang: str = "en",
    ) -> dict:
        params = {
            "lat": lat,
            "lon": lon,
            "appid": self.config.WEATHER_API_KEY,
            "units": units,
            "lang": lang,
        }
        async with ClientSession() as session:
            async with session.get(
                url=self.config.WEATHER_API, params=params
            ) as response:
                if response.status != 200:
                    raise HTTPException(
                        status_code=response.status,
                        detail=await response.text()
                    )
                response = await response.json()
                await self._save_history(
                    response=response, user=user, city=False
                )
                return response
