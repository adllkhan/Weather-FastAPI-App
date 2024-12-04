from pydantic import BaseModel


class History(BaseModel):
    city: str | None = None
    longitude: float | None = None
    latitude: float | None = None
    temperature: float
    description: str

    class Config:
        from_attributes = True


class Histories(BaseModel):
    histories: list[History]
