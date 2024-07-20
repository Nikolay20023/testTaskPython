from pydantic import BaseModel
import uuid


class WeatherCreate(BaseModel):
    city: str
    data: str
    user_id: uuid.UUID


class WeatherUpdate(WeatherCreate):
    pass