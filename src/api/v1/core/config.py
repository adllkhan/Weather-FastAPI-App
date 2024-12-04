from pydantic_settings import BaseSettings
from dotenv import load_dotenv


load_dotenv()


class Config(BaseSettings):
    WEATHER_API: str
    WEATHER_API_KEY: str
    POSTGRES_URL: str
    JWT_SECRET: str
    JWT_ALGORITHM: str
    SERVER_HOST: str
    SERVER_PORT: int
