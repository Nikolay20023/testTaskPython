from service.repository import RepositoryDB
from schemas.users import  UserCreate, UserUpdate
from schemas.weather import WeatherCreate, WeatherUpdate
from models.models import User, Weather


class RepositoryUser(RepositoryDB[User, UserCreate, UserUpdate]):
    pass


class RepositoryWeather(RepositoryDB[Weather, WeatherCreate, WeatherUpdate]):
    pass


user_crud = RepositoryUser(User)

weather_crud = RepositoryWeather(Weather)