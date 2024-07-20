from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
import aiohttp
from loguru import logger

from core.config import app_setting
from api.v1.users import get_current_user
from db.db import get_session
from service.users import weather_crud
from schemas.weather import WeatherCreate


router = APIRouter()


async def get_coordinates(city):
    params = {
        "q": city,
        "key": app_setting.api_key
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(app_setting.api_url_geocode, params=params) as response:
            if response.status == 200:
                data = await response.json()
                if data["results"]:
                    coordinates = data['results'][0]['geometry']
                    return coordinates['lat'], coordinates['lng']
            


async def get_weather_forecast(latitude, longitude):
    params = {
        'latitude': latitude,
        'longitude': longitude,
        'hourly': 'temperature_2m',
        'daily': 'temperature_2m_max,temperature_2m_min',
        'temperature_unit': 'celsius',
        'timezone': 'auto'
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(app_setting.api_urL_open_meteo, params=params) as response:
            if response.status == 200:
                data = await response.json()
                return data

@router.get("/weather")
async def get_weather(city: str, user = Depends(get_current_user), db: AsyncSession = Depends(get_session)):
    try:
        latitude, longitude = await get_coordinates(city=city)
        logger.info(latitude, longitude)
        forecast = await get_weather_forecast(latitude, longitude)
        logger.info(forecast)
        weather = WeatherCreate(city=city, data=forecast, user_id=user.id)
        new_weather = await weather_crud.create(db=db, obj_in=weather)
    except Exception as e:
        logger.error(e)
    
    return WeatherCreate(**new_weather.__dict__)